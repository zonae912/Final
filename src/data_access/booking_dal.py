# AI Contribution: Copilot generated booking DAL with conflict detection logic
# Reviewed and enhanced by team for complex availability checking

"""
Data Access Layer for Bookings
Encapsulates all database operations for the Booking model.
"""

from src.models.models import db, Booking, Resource
from datetime import datetime
from sqlalchemy import and_, or_


class BookingDAL:
    """Data Access Layer for Booking operations."""
    
    @staticmethod
    def create_booking(resource_id, requester_id, start_datetime, end_datetime,
                      purpose=None, notes=None):
        """
        Create a new booking.
        
        Args:
            resource_id (int): Resource to book
            requester_id (int): User making the booking
            start_datetime (datetime): Booking start time
            end_datetime (datetime): Booking end time
            purpose (str): Purpose of booking
            notes (str): Additional notes
            
        Returns:
            Booking: Created booking object or None if conflict exists
        """
        from src.models.models import Resource
        
        # Check for conflicts
        if BookingDAL.has_conflict(resource_id, start_datetime, end_datetime):
            return None
        
        # Get resource to check if approval is required
        resource = Resource.query.get(resource_id)
        
        # Automatic approval for open resources (study rooms)
        # Pending approval for restricted resources (classrooms, labs, equipment, event spaces)
        if resource and not resource.requires_approval:
            initial_status = 'approved'  # Auto-approve open resources like study rooms
        else:
            initial_status = 'pending'   # Require approval for restricted resources
        
        booking = Booking(
            resource_id=resource_id,
            requester_id=requester_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            status=initial_status,
            purpose=purpose,
            notes=notes
        )
        
        try:
            db.session.add(booking)
            db.session.commit()
            return booking
        except Exception:
            db.session.rollback()
            return None
    
    @staticmethod
    def has_conflict(resource_id, start_datetime, end_datetime, exclude_booking_id=None):
        """
        Check if a time slot has conflicting bookings.
        
        Args:
            resource_id (int): Resource ID to check
            start_datetime (datetime): Proposed start time
            end_datetime (datetime): Proposed end time
            exclude_booking_id (int): Booking ID to exclude from check (for updates)
            
        Returns:
            bool: True if conflict exists, False otherwise
        """
        query = Booking.query.filter(
            Booking.resource_id == resource_id,
            Booking.status.in_(['pending', 'approved']),
            or_(
                # New booking starts during existing booking
                and_(
                    Booking.start_datetime <= start_datetime,
                    Booking.end_datetime > start_datetime
                ),
                # New booking ends during existing booking
                and_(
                    Booking.start_datetime < end_datetime,
                    Booking.end_datetime >= end_datetime
                ),
                # New booking contains existing booking
                and_(
                    Booking.start_datetime >= start_datetime,
                    Booking.end_datetime <= end_datetime
                )
            )
        )
        
        if exclude_booking_id:
            query = query.filter(Booking.booking_id != exclude_booking_id)
        
        return query.first() is not None
    
    @staticmethod
    def get_booking_by_id(booking_id):
        """Get booking by ID."""
        return Booking.query.get(booking_id)
    
    @staticmethod
    def get_bookings_by_user(user_id, status=None):
        """
        Get all bookings made by a user.
        
        Args:
            user_id (int): User ID
            status (str): Optional status filter
            
        Returns:
            list: List of Booking objects
        """
        query = Booking.query.filter_by(requester_id=user_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Booking.start_datetime.desc()).all()
    
    @staticmethod
    def get_bookings_by_resource(resource_id, status=None):
        """
        Get all bookings for a resource.
        
        Args:
            resource_id (int): Resource ID
            status (str): Optional status filter
            
        Returns:
            list: List of Booking objects
        """
        query = Booking.query.filter_by(resource_id=resource_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Booking.start_datetime.desc()).all()
    
    @staticmethod
    def get_pending_bookings_for_owner(owner_id):
        """
        Get pending bookings for resources owned by a user.
        
        Args:
            owner_id (int): Resource owner user ID
            
        Returns:
            list: List of pending Booking objects
        """
        return db.session.query(Booking).join(Resource).filter(
            Resource.owner_id == owner_id,
            Booking.status == 'pending'
        ).order_by(Booking.created_at.desc()).all()
    
    @staticmethod
    def update_booking_status(booking_id, status, notes=None):
        """
        Update booking status.
        
        Args:
            booking_id (int): Booking ID
            status (str): New status (pending, approved, rejected, cancelled, completed)
            notes (str): Optional notes for status change
            
        Returns:
            Booking: Updated booking or None if not found
        """
        booking = Booking.query.get(booking_id)
        if not booking:
            return None
        
        booking.status = status
        if notes:
            booking.notes = notes
        booking.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            return booking
        except Exception:
            db.session.rollback()
            return None
    
    @staticmethod
    def update_booking(booking_id, **kwargs):
        """
        Update booking fields.
        
        Args:
            booking_id (int): Booking ID
            **kwargs: Fields to update
            
        Returns:
            Booking: Updated booking or None if not found or conflict
        """
        booking = Booking.query.get(booking_id)
        if not booking:
            return None
        
        # If updating time, check for conflicts
        if 'start_datetime' in kwargs or 'end_datetime' in kwargs:
            start = kwargs.get('start_datetime', booking.start_datetime)
            end = kwargs.get('end_datetime', booking.end_datetime)
            if BookingDAL.has_conflict(booking.resource_id, start, end, booking_id):
                return None
        
        # Update allowed fields
        allowed_fields = ['start_datetime', 'end_datetime', 'purpose', 'notes', 
                         'status', 'google_calendar_event_id']
        for field in allowed_fields:
            if field in kwargs:
                setattr(booking, field, kwargs[field])
        
        booking.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            return booking
        except Exception:
            db.session.rollback()
            return None
    
    @staticmethod
    def delete_booking(booking_id):
        """
        Delete a booking.
        
        Args:
            booking_id (int): Booking ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        booking = Booking.query.get(booking_id)
        if not booking:
            return False
        
        try:
            db.session.delete(booking)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def get_upcoming_bookings(user_id, limit=10):
        """
        Get upcoming approved bookings for a user.
        
        Args:
            user_id (int): User ID
            limit (int): Maximum number of bookings to return
            
        Returns:
            list: List of upcoming Booking objects
        """
        return Booking.query.filter(
            Booking.requester_id == user_id,
            Booking.status == 'approved',
            Booking.start_datetime > datetime.utcnow()
        ).order_by(Booking.start_datetime).limit(limit).all()
    
    @staticmethod
    def mark_past_bookings_complete():
        """
        Mark all past approved bookings as completed.
        
        Returns:
            int: Number of bookings updated
        """
        count = Booking.query.filter(
            Booking.status == 'approved',
            Booking.end_datetime < datetime.utcnow()
        ).update({Booking.status: 'completed'})
        
        try:
            db.session.commit()
            return count
        except Exception:
            db.session.rollback()
            return 0
