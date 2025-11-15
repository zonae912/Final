# AI Contribution: Copilot generated calendar controller with OAuth and iCal export
# Reviewed and enhanced by team for Google Calendar API integration

"""
Calendar Controller
Handles Google Calendar OAuth integration and iCal export functionality.
"""

from flask import Blueprint, redirect, url_for, flash, request, make_response, session, current_app
from flask_login import login_required, current_user
from datetime import datetime
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from icalendar import Calendar, Event as ICalEvent
import pytz

from src.data_access import UserDAL, BookingDAL, ResourceDAL

calendar_bp = Blueprint('calendar', __name__, url_prefix='/calendar')


def get_google_flow():
    """Create Google OAuth flow."""
    client_config = {
        "web": {
            "client_id": current_app.config['GOOGLE_CLIENT_ID'],
            "client_secret": current_app.config['GOOGLE_CLIENT_SECRET'],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [url_for('calendar.oauth_callback', _external=True)]
        }
    }
    
    flow = Flow.from_client_config(
        client_config,
        scopes=['https://www.googleapis.com/auth/calendar.events'],
        redirect_uri=url_for('calendar.oauth_callback', _external=True)
    )
    
    return flow


@calendar_bp.route('/connect')
@login_required
def connect():
    """Initiate Google Calendar OAuth flow."""
    try:
        flow = get_google_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # Store state in session for verification
        session['oauth_state'] = state
        
        return redirect(authorization_url)
    except Exception as e:
        flash(f'Failed to connect to Google Calendar: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard'))


@calendar_bp.route('/oauth/callback')
@login_required
def oauth_callback():
    """Handle Google OAuth callback."""
    # Verify state
    state = session.get('oauth_state')
    if not state or state != request.args.get('state'):
        flash('Invalid OAuth state. Please try again.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    try:
        flow = get_google_flow()
        flow.fetch_token(authorization_response=request.url)
        
        credentials = flow.credentials
        
        # Store tokens in database
        UserDAL.update_google_tokens(
            current_user.user_id,
            credentials.token,
            credentials.refresh_token,
            credentials.expiry
        )
        
        flash('Google Calendar connected successfully!', 'success')
    except Exception as e:
        flash(f'Failed to authorize Google Calendar: {str(e)}', 'danger')
    
    return redirect(url_for('main.dashboard'))


@calendar_bp.route('/disconnect', methods=['POST'])
@login_required
def disconnect():
    """Disconnect Google Calendar."""
    UserDAL.update_google_tokens(current_user.user_id, None, None, None)
    flash('Google Calendar disconnected.', 'info')
    return redirect(url_for('main.dashboard'))


@calendar_bp.route('/sync/<int:booking_id>', methods=['POST'])
@login_required
def sync_booking(booking_id):
    """Sync a booking to Google Calendar."""
    booking = BookingDAL.get_booking_by_id(booking_id)
    
    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Check permission
    if booking.requester_id != current_user.user_id:
        flash('You do not have permission to sync this booking.', 'danger')
        return redirect(url_for('booking.detail', booking_id=booking_id))
    
    # Check if user has connected Google Calendar
    if not current_user.google_calendar_token:
        flash('Please connect your Google Calendar first.', 'warning')
        return redirect(url_for('calendar.connect'))
    
    try:
        # Create credentials
        credentials = Credentials(
            token=current_user.google_calendar_token,
            refresh_token=current_user.google_refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=current_app.config['GOOGLE_CLIENT_ID'],
            client_secret=current_app.config['GOOGLE_CLIENT_SECRET']
        )
        
        # Build calendar service
        service = build('calendar', 'v3', credentials=credentials)
        
        # Get resource details
        resource = ResourceDAL.get_resource_by_id(booking.resource_id)
        
        # Create event
        event = {
            'summary': f'Booking: {resource.title}',
            'location': resource.location or '',
            'description': f'Booking for {resource.title}\\n\\nPurpose: {booking.purpose or "N/A"}\\n\\nNotes: {booking.notes or "N/A"}',
            'start': {
                'dateTime': booking.start_datetime.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': booking.end_datetime.isoformat(),
                'timeZone': 'UTC',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }
        
        # Insert event
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        
        # Update booking with event ID
        BookingDAL.update_booking(booking_id, google_calendar_event_id=created_event['id'])
        
        flash('Booking synced to Google Calendar!', 'success')
    except Exception as e:
        flash(f'Failed to sync booking: {str(e)}', 'danger')
    
    return redirect(url_for('booking.detail', booking_id=booking_id))


@calendar_bp.route('/export/<int:booking_id>.ics')
@login_required
def export_ical(booking_id):
    """Export booking as iCal file."""
    booking = BookingDAL.get_booking_by_id(booking_id)
    
    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Check permission
    if booking.requester_id != current_user.user_id:
        flash('You do not have permission to export this booking.', 'danger')
        return redirect(url_for('booking.detail', booking_id=booking_id))
    
    # Get resource details
    resource = ResourceDAL.get_resource_by_id(booking.resource_id)
    
    # Create iCal calendar
    cal = Calendar()
    cal.add('prodid', '-//Campus Resource Hub//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'Campus Resource Hub Booking')
    cal.add('x-wr-timezone', 'UTC')
    
    # Create event
    event = ICalEvent()
    event.add('summary', f'Booking: {resource.title}')
    event.add('dtstart', booking.start_datetime)
    event.add('dtend', booking.end_datetime)
    event.add('dtstamp', datetime.utcnow())
    event.add('uid', f'booking-{booking_id}@campushub.edu')
    
    if resource.location:
        event.add('location', resource.location)
    
    description = f'Booking for {resource.title}\\n\\n'
    if booking.purpose:
        description += f'Purpose: {booking.purpose}\\n'
    if booking.notes:
        description += f'Notes: {booking.notes}\\n'
    event.add('description', description)
    
    # Add status
    if booking.status == 'approved':
        event.add('status', 'CONFIRMED')
    elif booking.status == 'cancelled':
        event.add('status', 'CANCELLED')
    else:
        event.add('status', 'TENTATIVE')
    
    cal.add_component(event)
    
    # Create response
    response = make_response(cal.to_ical())
    response.headers['Content-Type'] = 'text/calendar; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename=booking-{booking_id}.ics'
    
    return response


@calendar_bp.route('/export-all.ics')
@login_required
def export_all_ical():
    """Export all user's approved bookings as iCal file."""
    bookings = BookingDAL.get_bookings_by_user(current_user.user_id, status='approved')
    
    # Create iCal calendar
    cal = Calendar()
    cal.add('prodid', '-//Campus Resource Hub//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'My Campus Resource Hub Bookings')
    cal.add('x-wr-timezone', 'UTC')
    
    # Add all bookings as events
    for booking in bookings:
        resource = ResourceDAL.get_resource_by_id(booking.resource_id)
        
        event = ICalEvent()
        event.add('summary', f'Booking: {resource.title}')
        event.add('dtstart', booking.start_datetime)
        event.add('dtend', booking.end_datetime)
        event.add('dtstamp', datetime.utcnow())
        event.add('uid', f'booking-{booking.booking_id}@campushub.edu')
        
        if resource.location:
            event.add('location', resource.location)
        
        description = f'Booking for {resource.title}\\n\\n'
        if booking.purpose:
            description += f'Purpose: {booking.purpose}\\n'
        event.add('description', description)
        event.add('status', 'CONFIRMED')
        
        cal.add_component(event)
    
    # Create response
    response = make_response(cal.to_ical())
    response.headers['Content-Type'] = 'text/calendar; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename=my-bookings.ics'
    
    return response
