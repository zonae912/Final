# AI Contribution: Copilot generated review DAL with rating aggregation
# Reviewed and approved by team

"""
Data Access Layer for Reviews
Encapsulates all database operations for the Review model.
"""

from src.models.models import db, Review, Booking
from datetime import datetime
from sqlalchemy import func


class ReviewDAL:
    """Data Access Layer for Review operations."""
    
    @staticmethod
    def create_review(resource_id, reviewer_id, rating, comment=None, booking_id=None):
        """
        Create a new review.
        
        Args:
            resource_id (int): Resource being reviewed
            reviewer_id (int): User writing the review
            rating (int): Rating (1-5)
            comment (str): Optional review text
            booking_id (int): Optional associated booking
            
        Returns:
            Review: Created review object
        """
        if rating < 1 or rating > 5:
            return None
        
        review = Review(
            resource_id=resource_id,
            reviewer_id=reviewer_id,
            rating=rating,
            comment=comment,
            booking_id=booking_id
        )
        
        try:
            db.session.add(review)
            db.session.commit()
            return review
        except Exception:
            db.session.rollback()
            return None
    
    @staticmethod
    def get_review_by_id(review_id):
        """Get review by ID."""
        return Review.query.get(review_id)
    
    @staticmethod
    def get_reviews_for_resource(resource_id, include_hidden=False):
        """
        Get all reviews for a resource.
        
        Args:
            resource_id (int): Resource ID
            include_hidden (bool): Whether to include hidden reviews
            
        Returns:
            list: List of Review objects
        """
        query = Review.query.filter_by(resource_id=resource_id)
        if not include_hidden:
            query = query.filter_by(is_hidden=False)
        return query.order_by(Review.timestamp.desc()).all()
    
    @staticmethod
    def get_reviews_by_user(reviewer_id):
        """
        Get all reviews written by a user.
        
        Args:
            reviewer_id (int): User ID
            
        Returns:
            list: List of Review objects
        """
        return Review.query.filter_by(reviewer_id=reviewer_id)\
            .order_by(Review.timestamp.desc()).all()
    
    @staticmethod
    def get_average_rating(resource_id):
        """
        Calculate average rating for a resource.
        
        Args:
            resource_id (int): Resource ID
            
        Returns:
            float: Average rating or 0 if no reviews
        """
        result = db.session.query(func.avg(Review.rating)).filter(
            Review.resource_id == resource_id,
            Review.is_hidden == False
        ).scalar()
        
        return float(result) if result else 0.0
    
    @staticmethod
    def get_rating_distribution(resource_id):
        """
        Get distribution of ratings for a resource.
        
        Args:
            resource_id (int): Resource ID
            
        Returns:
            dict: Distribution like {1: 2, 2: 0, 3: 5, 4: 10, 5: 8}
        """
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        results = db.session.query(Review.rating, func.count(Review.rating)).filter(
            Review.resource_id == resource_id,
            Review.is_hidden == False
        ).group_by(Review.rating).all()
        
        for rating, count in results:
            distribution[rating] = count
        
        return distribution
    
    @staticmethod
    def can_user_review(user_id, resource_id):
        """
        Check if a user can review a resource (must have completed booking).
        
        Args:
            user_id (int): User ID
            resource_id (int): Resource ID
            
        Returns:
            bool: True if user can review, False otherwise
        """
        # Check if user has a completed booking
        completed_booking = Booking.query.filter_by(
            requester_id=user_id,
            resource_id=resource_id,
            status='completed'
        ).first()
        
        if not completed_booking:
            return False
        
        # Check if user already reviewed this resource
        existing_review = Review.query.filter_by(
            reviewer_id=user_id,
            resource_id=resource_id
        ).first()
        
        return existing_review is None
    
    @staticmethod
    def has_user_reviewed(user_id, resource_id, booking_id=None):
        """
        Check if a user has already reviewed a resource/booking.
        
        Args:
            user_id (int): User ID
            resource_id (int): Resource ID
            booking_id (int): Optional booking ID for specific booking review
            
        Returns:
            bool: True if user has already reviewed, False otherwise
        """
        query = Review.query.filter_by(
            reviewer_id=user_id,
            resource_id=resource_id
        )
        
        if booking_id:
            query = query.filter_by(booking_id=booking_id)
        
        return query.first() is not None
    
    @staticmethod
    def update_review(review_id, rating=None, comment=None):
        """
        Update a review.
        
        Args:
            review_id (int): Review ID
            rating (int): New rating (1-5)
            comment (str): New comment
            
        Returns:
            Review: Updated review or None if not found
        """
        review = Review.query.get(review_id)
        if not review:
            return None
        
        if rating is not None:
            if rating < 1 or rating > 5:
                return None
            review.rating = rating
        
        if comment is not None:
            review.comment = comment
        
        try:
            db.session.commit()
            return review
        except Exception:
            db.session.rollback()
            return None
    
    @staticmethod
    def hide_review(review_id, hide=True):
        """
        Hide or unhide a review (admin moderation).
        
        Args:
            review_id (int): Review ID
            hide (bool): True to hide, False to unhide
            
        Returns:
            bool: True if successful, False otherwise
        """
        review = Review.query.get(review_id)
        if not review:
            return False
        
        review.is_hidden = hide
        
        try:
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def delete_review(review_id):
        """
        Delete a review.
        
        Args:
            review_id (int): Review ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        review = Review.query.get(review_id)
        if not review:
            return False
        
        try:
            db.session.delete(review)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def get_pending_reviews_for_user(user_id):
        """
        Get bookings that are completed but not yet reviewed by the user.
        
        Args:
            user_id (int): User ID
            
        Returns:
            list: List of Booking objects that can be reviewed
        """
        # Get completed bookings
        completed_bookings = Booking.query.filter_by(
            requester_id=user_id,
            status='completed'
        ).all()
        
        # Filter out bookings that already have reviews
        pending = []
        for booking in completed_bookings:
            existing_review = Review.query.filter_by(
                reviewer_id=user_id,
                resource_id=booking.resource_id,
                booking_id=booking.booking_id
            ).first()
            
            if not existing_review:
                pending.append(booking)
        
        return pending
