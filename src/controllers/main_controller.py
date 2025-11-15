# AI Contribution: Copilot generated main routes for homepage and dashboard
# Reviewed and approved by team

"""
Main Controller
Handles homepage, dashboard, and general application routes.
"""

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from datetime import datetime

from src.data_access import ResourceDAL, BookingDAL, MessageDAL, ReviewDAL
from src.models.models import Resource

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage with featured resources and search."""
    # Get specific featured resources (CG 1022-1050 lecture halls)
    featured_titles = [
        'CG 1022 Lecture Hall',
        'CG 1026 Lecture Hall',
        'CG 1032 Lecture Hall',
        'CG 1034 Lecture Hall',
        'CG 1040 Lecture Hall',
        'CG 1050 Lecture Hall'
    ]
    
    featured_resources = Resource.query.filter(
        Resource.title.in_(featured_titles),
        Resource.status == 'published'
    ).all()
    
    # Get categories for filter
    categories = ResourceDAL.get_categories()
    
    return render_template('index.html', 
                         featured_resources=featured_resources,
                         categories=categories)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing bookings, messages, and owned resources."""
    # Get user's bookings
    upcoming_bookings = BookingDAL.get_upcoming_bookings(current_user.user_id, limit=5)
    
    # Get pending bookings if user owns resources
    pending_approvals = []
    if current_user.is_staff():
        pending_approvals = BookingDAL.get_pending_bookings_for_owner(current_user.user_id)
    
    # Get user's resources
    my_resources = ResourceDAL.get_resources_by_owner(current_user.user_id)
    
    # Get unread message count
    unread_count = MessageDAL.get_unread_count(current_user.user_id)
    
    # Get pending reviews
    pending_reviews = ReviewDAL.get_pending_reviews_for_user(current_user.user_id)
    
    return render_template('dashboard.html',
                         upcoming_bookings=upcoming_bookings,
                         pending_approvals=pending_approvals,
                         my_resources=my_resources,
                         unread_count=unread_count,
                         pending_reviews=pending_reviews)


@main_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html')


@main_bp.route('/help')
def help_page():
    """Help/FAQ page."""
    return render_template('help.html')


@main_bp.route('/search')
def search():
    """Global search page."""
    from datetime import datetime
    
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    location = request.args.get('location', '')
    sort_by = request.args.get('sort', 'recent')
    capacity = request.args.get('capacity', type=int)
    
    # Parse availability dates
    start_date = request.args.get('start_date', '')
    start_time = request.args.get('start_time', '')
    end_date = request.args.get('end_date', '')
    end_time = request.args.get('end_time', '')
    
    start_datetime = None
    end_datetime = None
    
    # Parse datetime if provided
    if start_date and start_time:
        try:
            start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass
    
    if end_date and end_time:
        try:
            end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass
    
    # Search resources
    resources = ResourceDAL.search_resources(
        keyword=query if query else None,
        category=category if category else None,
        location=location if location else None,
        min_capacity=capacity,
        sort_by=sort_by,
        start_datetime=start_datetime,
        end_datetime=end_datetime
    )
    
    # Get categories for filter
    categories = ResourceDAL.get_categories()
    
    return render_template('search.html',
                         resources=resources,
                         query=query,
                         selected_category=category,
                         location=location,
                         sort_by=sort_by,
                         capacity=capacity,
                         start_date=start_date,
                         start_time=start_time,
                         end_date=end_date,
                         end_time=end_time,
                         categories=categories)


@main_bp.route('/calendar')
@login_required
def calendar_view():
    """Calendar view of user's bookings."""
    from datetime import timedelta
    
    # Get user's bookings
    my_bookings = BookingDAL.get_bookings_by_requester(current_user.user_id)
    
    # Get bookings for resources owned by user (if staff)
    owned_bookings = []
    if current_user.is_staff():
        my_resources = ResourceDAL.get_resources_by_owner(current_user.user_id)
        for resource in my_resources:
            owned_bookings.extend(BookingDAL.get_bookings_by_resource(resource.resource_id))
    
    return render_template('calendar.html',
                         my_bookings=my_bookings,
                         owned_bookings=owned_bookings)
