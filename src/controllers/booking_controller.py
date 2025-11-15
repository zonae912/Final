# AI Contribution: Copilot generated booking controller with conflict detection
# Reviewed and enhanced by team for calendar integration

"""
Booking Controller
Handles booking creation, approval, and management.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import bleach

from src.data_access import BookingDAL, ResourceDAL, MessageDAL
from src.models.models import db

booking_bp = Blueprint('booking', __name__, url_prefix='/bookings')


@booking_bp.route('/create/<int:resource_id>', methods=['GET', 'POST'])
@login_required
def create(resource_id):
    """Create a new booking for a resource."""
    resource = ResourceDAL.get_resource_by_id(resource_id)
    
    if not resource or resource.status != 'published':
        flash('Resource not found or not available.', 'danger')
        return redirect(url_for('resource.list_resources'))
    
    if request.method == 'POST':
        # Get form data
        start_date = request.form.get('start_date')
        start_time = request.form.get('start_time')
        end_date = request.form.get('end_date')
        end_time = request.form.get('end_time')
        purpose = bleach.clean(request.form.get('purpose', '').strip())
        notes = bleach.clean(request.form.get('notes', '').strip())
        
        # Recurrence parameters
        is_recurring = request.form.get('is_recurring') == 'on'
        recurrence_pattern = request.form.get('recurrence_pattern', 'weekly')
        recurrence_count = request.form.get('recurrence_count', type=int)
        recurrence_end_date = request.form.get('recurrence_end_date')
        
        # Validate and parse datetime
        try:
            start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            flash('Invalid date/time format.', 'danger')
            return render_template('bookings/create.html', resource=resource)
        
        # Validation
        errors = []
        
        if start_datetime < datetime.now():
            errors.append('Booking cannot be in the past.')
        
        if end_datetime <= start_datetime:
            errors.append('End time must be after start time.')
        
        if (end_datetime - start_datetime).total_seconds() / 3600 > 24:
            errors.append('Booking cannot exceed 24 hours.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('bookings/create.html', resource=resource)
        
        # Handle recurring bookings
        bookings_created = []
        conflicts = []
        
        if is_recurring and recurrence_count:
            from datetime import timedelta
            
            # Determine the interval
            if recurrence_pattern == 'daily':
                delta = timedelta(days=1)
            elif recurrence_pattern == 'weekly':
                delta = timedelta(weeks=1)
            elif recurrence_pattern == 'biweekly':
                delta = timedelta(weeks=2)
            else:
                delta = timedelta(weeks=1)
            
            # Create recurring bookings
            current_start = start_datetime
            current_end = end_datetime
            
            for i in range(min(recurrence_count, 10)):  # Max 10 occurrences
                # Check if we've passed the end date
                if recurrence_end_date:
                    try:
                        end_by = datetime.strptime(recurrence_end_date, "%Y-%m-%d")
                        if current_start.date() > end_by.date():
                            break
                    except ValueError:
                        pass
                
                # Try to create booking
                booking = BookingDAL.create_booking(
                    resource_id=resource_id,
                    requester_id=current_user.user_id,
                    start_datetime=current_start,
                    end_datetime=current_end,
                    purpose=purpose,
                    notes=notes
                )
                
                if booking:
                    bookings_created.append(booking)
                else:
                    conflicts.append(current_start.strftime('%Y-%m-%d %H:%M'))
                
                # Move to next occurrence
                current_start += delta
                current_end += delta
            
            # Show results
            if bookings_created:
                # Send notifications for pending bookings
                if bookings_created[0].status == 'pending':
                    MessageDAL.create_message(
                        sender_id=current_user.user_id,
                        receiver_id=resource.owner_id,
                        content=f"{len(bookings_created)} recurring booking requests for '{resource.title}'. Please review and approve.",
                        related_booking_id=bookings_created[0].booking_id
                    )
                
                message = f"Successfully created {len(bookings_created)} recurring bookings!"
                if conflicts:
                    message += f" ({len(conflicts)} time slots had conflicts and were skipped)"
                
                flash(message, 'success')
                return redirect(url_for('booking.my_bookings'))
            else:
                flash('All recurring time slots have conflicts. Please choose different times.', 'danger')
                return render_template('bookings/create.html', resource=resource)
        
        # Single booking (non-recurring)
        
        # Create booking
        booking = BookingDAL.create_booking(
            resource_id=resource_id,
            requester_id=current_user.user_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            purpose=purpose,
            notes=notes
        )
        
        if booking:
            # Send notification based on approval status
            if booking.status == 'approved':
                # Auto-approved (open resource like study room)
                flash('Booking confirmed! Your reservation has been automatically approved.', 'success')
            else:
                # Requires approval (restricted resource like classroom)
                MessageDAL.create_message(
                    sender_id=current_user.user_id,
                    receiver_id=resource.owner_id,
                    content=f"New booking request for '{resource.title}' from {start_datetime.strftime('%Y-%m-%d %H:%M')} to {end_datetime.strftime('%Y-%m-%d %H:%M')}. Please review and approve.",
                    related_booking_id=booking.booking_id
                )
                flash('Booking request submitted! It is pending approval from the resource owner or administrator.', 'info')
            
            return redirect(url_for('booking.detail', booking_id=booking.booking_id))
        else:
            flash('Booking conflict detected. Please choose a different time.', 'danger')
    
    return render_template('bookings/create.html', resource=resource)


@booking_bp.route('/<int:booking_id>')
@login_required
def detail(booking_id):
    """View booking details."""
    booking = BookingDAL.get_booking_by_id(booking_id)
    
    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Check access permission
    resource = ResourceDAL.get_resource_by_id(booking.resource_id)
    if booking.requester_id != current_user.user_id and \
       resource.owner_id != current_user.user_id and \
       not current_user.is_admin():
        flash('You do not have permission to view this booking.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    return render_template('bookings/detail.html', 
                         booking=booking,
                         resource=resource)


@booking_bp.route('/<int:booking_id>/approve', methods=['POST'])
@login_required
def approve(booking_id):
    """Approve a booking request."""
    booking = BookingDAL.get_booking_by_id(booking_id)
    
    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    resource = ResourceDAL.get_resource_by_id(booking.resource_id)
    
    # Check permission (resource owner, staff, or admin)
    if resource.owner_id != current_user.user_id and not current_user.is_staff():
        flash('You do not have permission to approve this booking.', 'danger')
        return redirect(url_for('booking.detail', booking_id=booking_id))
    
    # Update status
    updated = BookingDAL.update_booking_status(booking_id, 'approved')
    
    if updated:
        # Send notification to requester
        MessageDAL.create_message(
            sender_id=current_user.user_id,
            receiver_id=booking.requester_id,
            content=f"Your booking for '{resource.title}' has been approved!",
            related_booking_id=booking_id
        )
        
        flash('Booking approved successfully!', 'success')
    else:
        flash('Failed to approve booking.', 'danger')
    
    return redirect(url_for('booking.detail', booking_id=booking_id))


@booking_bp.route('/<int:booking_id>/reject', methods=['POST'])
@login_required
def reject(booking_id):
    """Reject a booking request."""
    booking = BookingDAL.get_booking_by_id(booking_id)
    
    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    resource = ResourceDAL.get_resource_by_id(booking.resource_id)
    
    # Check permission
    if resource.owner_id != current_user.user_id and not current_user.is_staff():
        flash('You do not have permission to reject this booking.', 'danger')
        return redirect(url_for('booking.detail', booking_id=booking_id))
    
    reason = bleach.clean(request.form.get('reason', 'No reason provided.'))
    
    # Update status
    updated = BookingDAL.update_booking_status(booking_id, 'rejected', notes=reason)
    
    if updated:
        # Send notification to requester
        MessageDAL.create_message(
            sender_id=current_user.user_id,
            receiver_id=booking.requester_id,
            content=f"Your booking for '{resource.title}' was rejected. Reason: {reason}",
            related_booking_id=booking_id
        )
        
        flash('Booking rejected.', 'info')
    else:
        flash('Failed to reject booking.', 'danger')
    
    return redirect(url_for('booking.detail', booking_id=booking_id))


@booking_bp.route('/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel(booking_id):
    """Cancel a booking."""
    booking = BookingDAL.get_booking_by_id(booking_id)
    
    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Check permission (requester or admin)
    if booking.requester_id != current_user.user_id and not current_user.is_admin():
        flash('You do not have permission to cancel this booking.', 'danger')
        return redirect(url_for('booking.detail', booking_id=booking_id))
    
    # Update status
    updated = BookingDAL.update_booking_status(booking_id, 'cancelled')
    
    if updated:
        resource = ResourceDAL.get_resource_by_id(booking.resource_id)
        # Notify resource owner
        MessageDAL.create_message(
            sender_id=current_user.user_id,
            receiver_id=resource.owner_id,
            content=f"Booking for '{resource.title}' has been cancelled.",
            related_booking_id=booking_id
        )
        
        flash('Booking cancelled successfully.', 'info')
    else:
        flash('Failed to cancel booking.', 'danger')
    
    return redirect(url_for('main.dashboard'))


@booking_bp.route('/my-bookings')
@login_required
def my_bookings():
    """List current user's bookings."""
    from src.data_access import ReviewDAL
    
    # Mark past bookings as completed
    BookingDAL.mark_past_bookings_complete()
    
    bookings = BookingDAL.get_bookings_by_user(current_user.user_id)
    
    # Check which completed bookings need reviews
    needs_review = []
    for booking in bookings:
        if booking.status == 'completed':
            # Check if user has already reviewed
            has_reviewed = ReviewDAL.has_user_reviewed(current_user.user_id, booking.resource_id, booking.booking_id)
            if not has_reviewed:
                needs_review.append(booking.booking_id)
    
    return render_template('bookings/my_bookings.html', 
                         bookings=bookings,
                         needs_review=needs_review)


@booking_bp.route('/api/check-availability/<int:resource_id>')
@login_required
def check_availability(resource_id):
    """API endpoint to check booking availability (returns JSON)."""
    start_str = request.args.get('start')
    end_str = request.args.get('end')
    
    try:
        start_datetime = datetime.fromisoformat(start_str)
        end_datetime = datetime.fromisoformat(end_str)
    except:
        return jsonify({'available': False, 'message': 'Invalid date format'}), 400
    
    has_conflict = BookingDAL.has_conflict(resource_id, start_datetime, end_datetime)
    
    return jsonify({
        'available': not has_conflict,
        'message': 'Time slot is available' if not has_conflict else 'Time slot is already booked'
    })
