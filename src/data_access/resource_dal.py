# AI Contribution: Copilot generated resource CRUD with search functionality
# Reviewed and enhanced by team for filtering and sorting capabilities

"""
Data Access Layer for Resources
Encapsulates all database operations for the Resource model.
"""

from src.models.models import db, Resource
from datetime import datetime
import json
from sqlalchemy import or_, and_


class ResourceDAL:
    """Data Access Layer for Resource operations."""
    
    @staticmethod
    def create_resource(owner_id, title, description=None, category=None, 
                       location=None, capacity=None, images=None, 
                       availability_rules=None, requires_approval=False,
                       equipment_list=None, status='draft'):
        """
        Create a new resource.
        
        Args:
            owner_id (int): User ID of resource owner
            title (str): Resource title
            description (str): Resource description
            category (str): Resource category
            location (str): Resource location
            capacity (int): Resource capacity
            images (list): List of image paths
            availability_rules (dict): Availability rules as dict
            requires_approval (bool): Whether bookings require approval
            equipment_list (list): List of equipment
            status (str): Resource status (draft, published, archived)
            
        Returns:
            Resource: Created resource object
        """
        resource = Resource(
            owner_id=owner_id,
            title=title,
            description=description,
            category=category,
            location=location,
            capacity=capacity,
            images=json.dumps(images) if images else None,
            availability_rules=json.dumps(availability_rules) if availability_rules else None,
            requires_approval=requires_approval,
            equipment_list=json.dumps(equipment_list) if equipment_list else None,
            status=status
        )
        
        try:
            db.session.add(resource)
            db.session.commit()
            return resource
        except Exception:
            db.session.rollback()
            return None
    
    @staticmethod
    def get_resource_by_id(resource_id):
        """Get resource by ID."""
        return Resource.query.get(resource_id)
    
    @staticmethod
    def get_all_resources(status='published'):
        """
        Get all resources filtered by status.
        
        Args:
            status (str): Filter by status (None for all)
            
        Returns:
            list: List of Resource objects
        """
        query = Resource.query
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Resource.created_at.desc()).all()
    
    @staticmethod
    def get_resources_by_owner(owner_id):
        """Get all resources owned by a specific user."""
        return Resource.query.filter_by(owner_id=owner_id)\
            .order_by(Resource.created_at.desc()).all()
    
    @staticmethod
    def search_resources(keyword=None, category=None, location=None, 
                        min_capacity=None, sort_by='recent', status='published',
                        start_datetime=None, end_datetime=None):
        """
        Search and filter resources.
        
        Args:
            keyword (str): Search keyword for title/description
            category (str): Filter by category
            location (str): Filter by location
            min_capacity (int): Minimum capacity required
            sort_by (str): Sort option (recent, most_booked, top_rated)
            status (str): Filter by status
            start_datetime (datetime): Start of availability window
            end_datetime (datetime): End of availability window
            
        Returns:
            list: List of matching Resource objects
        """
        from src.models.models import Booking, Review
        from sqlalchemy import func
        
        query = Resource.query
        
        # Status filter
        if status:
            query = query.filter_by(status=status)
        
        # Keyword search
        if keyword:
            search = f"%{keyword}%"
            query = query.filter(
                or_(
                    Resource.title.ilike(search),
                    Resource.description.ilike(search),
                    Resource.location.ilike(search)
                )
            )
        
        # Category filter
        if category:
            query = query.filter_by(category=category)
        
        # Location filter
        if location:
            query = query.filter(Resource.location.ilike(f"%{location}%"))
        
        # Capacity filter
        if min_capacity:
            query = query.filter(Resource.capacity >= min_capacity)
        
        # Availability filter - exclude resources with conflicting bookings
        if start_datetime and end_datetime:
            # Get resource IDs that have conflicting bookings
            conflicting_bookings = db.session.query(Booking.resource_id).filter(
                and_(
                    Booking.status.in_(['approved', 'pending']),
                    or_(
                        # Booking starts during requested time
                        and_(
                            Booking.start_datetime >= start_datetime,
                            Booking.start_datetime < end_datetime
                        ),
                        # Booking ends during requested time
                        and_(
                            Booking.end_datetime > start_datetime,
                            Booking.end_datetime <= end_datetime
                        ),
                        # Booking spans entire requested time
                        and_(
                            Booking.start_datetime <= start_datetime,
                            Booking.end_datetime >= end_datetime
                        )
                    )
                )
            ).distinct()
            
            conflicting_ids = [b[0] for b in conflicting_bookings.all()]
            if conflicting_ids:
                query = query.filter(~Resource.resource_id.in_(conflicting_ids))
        
        # Sorting
        if sort_by == 'recent':
            query = query.order_by(Resource.created_at.desc())
        elif sort_by == 'title':
            query = query.order_by(Resource.title)
        elif sort_by == 'most_booked':
            # Join with bookings and count
            query = query.outerjoin(Booking).group_by(Resource.resource_id)\
                .order_by(func.count(Booking.booking_id).desc())
        elif sort_by == 'top_rated':
            # Join with reviews and calculate average rating
            query = query.outerjoin(Review).group_by(Resource.resource_id)\
                .order_by(func.coalesce(func.avg(Review.rating), 0).desc())
        
        return query.all()
    
    @staticmethod
    def update_resource(resource_id, **kwargs):
        """
        Update resource fields.
        
        Args:
            resource_id (int): Resource ID to update
            **kwargs: Fields to update
            
        Returns:
            Resource: Updated resource object or None if not found
        """
        resource = Resource.query.get(resource_id)
        if not resource:
            return None
        
        # Update allowed fields
        allowed_fields = ['title', 'description', 'category', 'location', 
                         'capacity', 'status', 'requires_approval']
        for field in allowed_fields:
            if field in kwargs:
                setattr(resource, field, kwargs[field])
        
        # Handle JSON fields
        if 'images' in kwargs:
            resource.images = json.dumps(kwargs['images'])
        if 'availability_rules' in kwargs:
            resource.availability_rules = json.dumps(kwargs['availability_rules'])
        if 'equipment_list' in kwargs:
            resource.equipment_list = json.dumps(kwargs['equipment_list'])
        
        resource.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            return resource
        except Exception:
            db.session.rollback()
            return None
    
    @staticmethod
    def delete_resource(resource_id):
        """
        Delete a resource.
        
        Args:
            resource_id (int): Resource ID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        resource = Resource.query.get(resource_id)
        if not resource:
            return False
        
        try:
            db.session.delete(resource)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def get_top_rated_resources(limit=10, min_rating=4.0, min_reviews=3):
        """
        Get top rated resources with minimum rating and review count.
        
        Args:
            limit (int): Number of resources to return
            min_rating (float): Minimum average rating
            min_reviews (int): Minimum number of reviews required
            
        Returns:
            list: List of tuples (Resource, avg_rating, review_count)
        """
        from src.models.models import Review
        from sqlalchemy import func
        
        # Query resources with their average rating and review count
        results = db.session.query(
            Resource,
            func.avg(Review.rating).label('avg_rating'),
            func.count(Review.review_id).label('review_count')
        ).join(
            Review, Resource.resource_id == Review.resource_id
        ).filter(
            Resource.status == 'published',
            Review.is_hidden == False
        ).group_by(
            Resource.resource_id
        ).having(
            func.avg(Review.rating) >= min_rating,
            func.count(Review.review_id) >= min_reviews
        ).order_by(
            func.avg(Review.rating).desc(),
            func.count(Review.review_id).desc()
        ).limit(limit).all()
        
        return results
    
    @staticmethod
    def get_resource_rating_badge(resource_id):
        """
        Get rating badge for a resource based on ratings.
        
        Args:
            resource_id (int): Resource ID
            
        Returns:
            dict: Badge info with 'name', 'class', 'icon' or None
        """
        from src.data_access import ReviewDAL
        
        avg_rating = ReviewDAL.get_average_rating(resource_id)
        review_count = len(ReviewDAL.get_reviews_for_resource(resource_id))
        
        # No badge if too few reviews
        if review_count < 3:
            return None
        
        # Top Rated: 4.5+ stars with 5+ reviews
        if avg_rating >= 4.5 and review_count >= 5:
            return {
                'name': 'Top Rated',
                'class': 'badge bg-success',
                'icon': 'bi-star-fill',
                'description': 'Highly rated by users'
            }
        
        # Excellent: 4.0+ stars with 3+ reviews
        if avg_rating >= 4.0 and review_count >= 3:
            return {
                'name': 'Excellent',
                'class': 'badge bg-primary',
                'icon': 'bi-star',
                'description': 'Consistently good ratings'
            }
        
        return None
    
    @staticmethod
    def get_categories():
        """Get list of unique categories."""
        categories = db.session.query(Resource.category)\
            .filter(Resource.category.isnot(None))\
            .filter(Resource.status == 'published')\
            .distinct().all()
        return [cat[0] for cat in categories]
    
    @staticmethod
    def get_top_rated_resources(limit=10):
        """
        Get top rated resources.
        
        Args:
            limit (int): Number of resources to return
            
        Returns:
            list: List of top rated resources
        """
        # This is a simplified version - actual implementation would calculate average ratings
        return Resource.query.filter_by(status='published')\
            .order_by(Resource.created_at.desc())\
            .limit(limit).all()
    
    @staticmethod
    def parse_json_field(resource, field_name):
        """
        Parse JSON field from resource.
        
        Args:
            resource (Resource): Resource object
            field_name (str): Name of JSON field
            
        Returns:
            list/dict: Parsed JSON data or empty list/dict
        """
        field_value = getattr(resource, field_name, None)
        if not field_value:
            return [] if field_name in ['images', 'equipment_list'] else {}
        try:
            return json.loads(field_value)
        except:
            return [] if field_name in ['images', 'equipment_list'] else {}
