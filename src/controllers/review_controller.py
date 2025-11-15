# AI Contribution: Copilot generated review controller with rating validation
# Reviewed and approved by team

"""
Review Controller
Handles resource reviews and ratings.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
import bleach

from src.data_access import ReviewDAL, ResourceDAL, BookingDAL

review_bp = Blueprint('review', __name__, url_prefix='/reviews')


@review_bp.route('/create/<int:resource_id>', methods=['GET', 'POST'])
@login_required
def create(resource_id):
    """Create a review for a resource."""
    resource = ResourceDAL.get_resource_by_id(resource_id)
    
    if not resource:
        flash('Resource not found.', 'danger')
        return redirect(url_for('resource.list_resources'))
    
    # Check if user can review
    if not ReviewDAL.can_user_review(current_user.user_id, resource_id):
        flash('You cannot review this resource. You must have a completed booking.', 'danger')
        return redirect(url_for('resource.detail', resource_id=resource_id))
    
    # Get booking ID from query parameter
    booking_id = request.args.get('booking_id', type=int)
    booking = None
    
    if booking_id:
        booking = BookingDAL.get_booking_by_id(booking_id)
        # Verify the booking belongs to the current user and is for this resource
        if not booking or booking.requester_id != current_user.user_id or booking.resource_id != resource_id:
            flash('Invalid booking specified.', 'danger')
            return redirect(url_for('resource.detail', resource_id=resource_id))
    
    if request.method == 'POST':
        rating = request.form.get('rating', type=int)
        comment = bleach.clean(request.form.get('comment', '').strip())
        
        # Validation
        if not rating or rating < 1 or rating > 5:
            flash('Please provide a valid rating (1-5).', 'danger')
            return render_template('reviews/create.html', resource=resource, booking=booking)
        
        # Get booking ID from form if provided
        form_booking_id = request.form.get('booking_id', type=int)
        
        review = ReviewDAL.create_review(
            resource_id=resource_id,
            reviewer_id=current_user.user_id,
            rating=rating,
            comment=comment,
            booking_id=form_booking_id
        )
        
        if review:
            flash('Review submitted successfully!', 'success')
            return redirect(url_for('resource.detail', resource_id=resource_id))
        else:
            flash('Failed to submit review.', 'danger')
    
    # Get user's completed bookings for this resource
    completed_bookings = BookingDAL.get_bookings_by_user(current_user.user_id, status='completed')
    resource_bookings = [b for b in completed_bookings if b.resource_id == resource_id]
    
    return render_template('reviews/create.html', 
                         resource=resource,
                         booking=booking,
                         bookings=resource_bookings)


@review_bp.route('/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(review_id):
    """Edit an existing review."""
    review = ReviewDAL.get_review_by_id(review_id)
    
    if not review:
        flash('Review not found.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Check ownership
    if review.reviewer_id != current_user.user_id:
        flash('You do not have permission to edit this review.', 'danger')
        return redirect(url_for('resource.detail', resource_id=review.resource_id))
    
    resource = ResourceDAL.get_resource_by_id(review.resource_id)
    
    if request.method == 'POST':
        rating = request.form.get('rating', type=int)
        comment = bleach.clean(request.form.get('comment', '').strip())
        
        if not rating or rating < 1 or rating > 5:
            flash('Please provide a valid rating (1-5).', 'danger')
            return render_template('reviews/edit.html', review=review, resource=resource)
        
        updated = ReviewDAL.update_review(review_id, rating=rating, comment=comment)
        
        if updated:
            flash('Review updated successfully!', 'success')
            return redirect(url_for('resource.detail', resource_id=review.resource_id))
        else:
            flash('Failed to update review.', 'danger')
    
    return render_template('reviews/edit.html', review=review, resource=resource)


@review_bp.route('/<int:review_id>/delete', methods=['POST'])
@login_required
def delete(review_id):
    """Delete a review."""
    review = ReviewDAL.get_review_by_id(review_id)
    
    if not review:
        flash('Review not found.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Check ownership or admin
    if review.reviewer_id != current_user.user_id and not current_user.is_admin():
        flash('You do not have permission to delete this review.', 'danger')
        return redirect(url_for('resource.detail', resource_id=review.resource_id))
    
    resource_id = review.resource_id
    
    if ReviewDAL.delete_review(review_id):
        flash('Review deleted successfully.', 'info')
    else:
        flash('Failed to delete review.', 'danger')
    
    return redirect(url_for('resource.detail', resource_id=resource_id))


@review_bp.route('/my-reviews')
@login_required
def my_reviews():
    """List current user's reviews."""
    reviews = ReviewDAL.get_reviews_by_user(current_user.user_id)
    return render_template('reviews/my_reviews.html', reviews=reviews)
