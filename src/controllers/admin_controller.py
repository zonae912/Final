# AI Contribution: Copilot generated admin controller with comprehensive management features
# Reviewed and enhanced by team for security and audit logging

"""
Admin Controller
Handles administrative functions for user, resource, booking, and review management.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
import bleach

from src.data_access import (UserDAL, ResourceDAL, BookingDAL, 
                            MessageDAL, ReviewDAL, AdminLogDAL)
from src.models.models import db, Booking

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin privileges."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics and recent activity."""
    from datetime import date
    
    # Get statistics
    total_users = len(UserDAL.get_all_users())
    total_resources = len(ResourceDAL.get_all_resources(status=None))
    active_resources = len(ResourceDAL.get_all_resources(status='published'))
    
    # Get pending bookings
    pending_bookings = Booking.query.filter_by(status='pending').count()
    
    # Get today's bookings
    today = date.today()
    todays_bookings = Booking.query.filter(
        db.func.date(Booking.start_datetime) == today
    ).count()
    
    # Get upcoming bookings
    upcoming_bookings = Booking.query.filter(
        Booking.start_datetime > datetime.now(),
        Booking.status.in_(['approved', 'pending'])
    ).count()
    
    # Get new users today (using User model)
    from src.models.models import User
    new_users_today = User.query.filter(
        db.func.date(User.created_at) == today
    ).count()
    
    # Create stats dictionary
    stats = {
        'total_users': total_users,
        'new_users_today': new_users_today,
        'active_resources': active_resources,
        'total_resources': total_resources,
        'pending_bookings': pending_bookings,
        'todays_bookings': todays_bookings,
        'upcoming_bookings': upcoming_bookings,
        'resource_utilization': min(100, int((todays_bookings / max(active_resources, 1)) * 100)),
        'user_engagement': min(100, int((todays_bookings / max(total_users, 1)) * 100 * 10)),
        'booking_success_rate': 85  # Placeholder
    }
    
    # Get recent admin actions
    recent_logs = AdminLogDAL.get_recent_logs(limit=20)
    
    # Get action statistics
    action_stats = AdminLogDAL.get_action_statistics(days=30)
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_logs=recent_logs,
                         action_stats=action_stats)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Manage users."""
    role_filter = request.args.get('role', '')
    search_query = request.args.get('q', '')
    
    if search_query:
        users_list = UserDAL.search_users(search_query, role=role_filter if role_filter else None)
    else:
        users_list = UserDAL.get_all_users(role=role_filter if role_filter else None)
    
    return render_template('admin/users.html', 
                         users=users_list,
                         search_query=search_query,
                         role_filter=role_filter)


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Edit user details."""
    user = UserDAL.get_user_by_id(user_id)
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.users'))
    
    if request.method == 'POST':
        name = bleach.clean(request.form.get('name', '').strip())
        role = request.form.get('role', '')
        department = bleach.clean(request.form.get('department', '').strip())
        
        if role not in ['student', 'staff', 'admin']:
            flash('Invalid role selected.', 'danger')
            return render_template('admin/edit_user.html', user=user)
        
        updated = UserDAL.update_user(
            user_id,
            name=name,
            role=role,
            department=department
        )
        
        if updated:
            # Log admin action
            AdminLogDAL.create_log(
                admin_id=current_user.user_id,
                action='user_update',
                target_table='users',
                target_id=user_id,
                details={'name': name, 'role': role, 'department': department}
            )
            
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.users'))
        else:
            flash('Failed to update user.', 'danger')
    
    return render_template('admin/edit_user.html', user=user)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user."""
    if user_id == current_user.user_id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
    
    user = UserDAL.get_user_by_id(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.users'))
    
    if UserDAL.delete_user(user_id):
        # Log admin action
        AdminLogDAL.create_log(
            admin_id=current_user.user_id,
            action='user_delete',
            target_table='users',
            target_id=user_id,
            details={'email': user.email, 'name': user.name}
        )
        
        flash('User deleted successfully.', 'info')
    else:
        flash('Failed to delete user.', 'danger')
    
    return redirect(url_for('admin.users'))


@admin_bp.route('/resources')
@login_required
@admin_required
def resources():
    """Manage resources."""
    status_filter = request.args.get('status', '')
    resources_list = ResourceDAL.get_all_resources(status=status_filter if status_filter else None)
    
    return render_template('admin/resources.html', 
                         resources=resources_list,
                         status_filter=status_filter)


@admin_bp.route('/bookings')
@login_required
@admin_required
def bookings():
    """Manage bookings."""
    status_filter = request.args.get('status', '')
    
    # Get all bookings (simplified - in production would paginate)
    from src.models.models import Booking
    query = Booking.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    bookings_list = query.order_by(Booking.created_at.desc()).limit(100).all()
    
    return render_template('admin/bookings.html', 
                         bookings=bookings_list,
                         status_filter=status_filter)


@admin_bp.route('/bookings/<int:booking_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_booking(booking_id):
    """Approve a pending booking."""
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.status != 'pending':
        flash('This booking has already been processed.', 'warning')
        return redirect(request.referrer or url_for('admin.bookings'))
    
    # Update booking status
    booking.status = 'approved'
    db.session.commit()
    
    # Log the action
    AdminLogDAL.create_log(
        admin_id=current_user.user_id,
        action='approve',
        target_table='booking',
        target_id=booking_id,
        details=f'Approved booking for {booking.resource.title}'
    )
    
    # Send notification to requester
    from src.models.models import Message
    notification = Message(
        sender_id=current_user.user_id,
        receiver_id=booking.requester_id,
        content=f'Your booking for "{booking.resource.title}" has been approved! Start: {booking.start_datetime.strftime("%Y-%m-%d %I:%M %p")}',
        related_booking_id=booking_id
    )
    db.session.add(notification)
    db.session.commit()
    
    flash(f'Booking #{booking_id} approved successfully!', 'success')
    return redirect(request.referrer or url_for('admin.bookings'))


@admin_bp.route('/bookings/<int:booking_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_booking(booking_id):
    """Reject a pending booking."""
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.status != 'pending':
        flash('This booking has already been processed.', 'warning')
        return redirect(request.referrer or url_for('admin.bookings'))
    
    reason = request.form.get('reason', 'No reason provided')
    
    # Update booking status
    booking.status = 'rejected'
    db.session.commit()
    
    # Log the action
    AdminLogDAL.create_log(
        admin_id=current_user.user_id,
        action='reject',
        target_table='booking',
        target_id=booking_id,
        details=f'Rejected booking for {booking.resource.title}. Reason: {reason}'
    )
    
    # Send notification to requester
    from src.models.models import Message
    notification = Message(
        sender_id=current_user.user_id,
        receiver_id=booking.requester_id,
        content=f'Your booking for "{booking.resource.title}" has been rejected. Reason: {reason}',
        related_booking_id=booking_id
    )
    db.session.add(notification)
    db.session.commit()
    
    flash(f'Booking #{booking_id} rejected.', 'info')
    return redirect(request.referrer or url_for('admin.bookings'))


@admin_bp.route('/reviews')
@login_required
@admin_required
def reviews():
    """Manage reviews."""
    # Get all reviews (simplified)
    from src.models.models import Review
    reviews_list = Review.query.order_by(Review.timestamp.desc()).limit(100).all()
    
    return render_template('admin/reviews.html', reviews=reviews_list)


@admin_bp.route('/reviews/<int:review_id>/hide', methods=['POST'])
@login_required
@admin_required
def hide_review(review_id):
    """Hide or unhide a review."""
    review = ReviewDAL.get_review_by_id(review_id)
    
    if not review:
        flash('Review not found.', 'danger')
        return redirect(url_for('admin.reviews'))
    
    hide = not review.is_hidden
    
    if ReviewDAL.hide_review(review_id, hide):
        action = 'hide' if hide else 'unhide'
        
        # Log admin action
        AdminLogDAL.create_log(
            admin_id=current_user.user_id,
            action=f'review_{action}',
            target_table='reviews',
            target_id=review_id,
            details={'resource_id': review.resource_id, 'reviewer_id': review.reviewer_id}
        )
        
        flash(f'Review {"hidden" if hide else "unhidden"} successfully.', 'success')
    else:
        flash('Failed to update review.', 'danger')
    
    return redirect(url_for('admin.reviews'))


@admin_bp.route('/logs')
@login_required
@admin_required
def logs():
    """View admin action logs."""
    action_filter = request.args.get('action', '')
    
    if action_filter:
        logs_list = AdminLogDAL.get_logs_by_action(action_filter, limit=100)
    else:
        logs_list = AdminLogDAL.get_recent_logs(limit=100)
    
    return render_template('admin/logs.html', 
                         logs=logs_list,
                         action_filter=action_filter)


@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    """View system analytics and reports."""
    # Get date range from query params
    days = request.args.get('days', 30, type=int)
    
    # Get statistics
    action_stats = AdminLogDAL.get_action_statistics(days=days)
    
    # Get resource usage statistics (simplified)
    from src.models.models import Resource, Booking
    top_resources = db.session.query(Resource, db.func.count(Booking.booking_id))\
        .join(Booking)\
        .group_by(Resource.resource_id)\
        .order_by(db.func.count(Booking.booking_id).desc())\
        .limit(10).all()
    
    return render_template('admin/analytics.html',
                         action_stats=action_stats,
                         top_resources=top_resources,
                         days=days)
