# Unit tests for booking logic - conflict detection and status transitions
# Tests booking DAL operations independently from Flask routes

"""
Test suite for Booking Logic
Tests conflict detection, status transitions, and CRUD operations.
"""

import pytest
from datetime import datetime, timedelta
from src import create_app
from src.models.models import db, User, Resource, Booking
from src.data_access import UserDAL, ResourceDAL, BookingDAL


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    with app.app_context():
        user = UserDAL.create_user(
            name='Test Student',
            email='student@test.edu',
            password='password123',
            role='student'
        )
        return user.user_id


@pytest.fixture
def sample_resource(app, sample_user):
    """Create a sample resource for testing."""
    with app.app_context():
        owner = UserDAL.create_user(
            name='Test Owner',
            email='owner@test.edu',
            password='password123',
            role='staff'
        )
        resource = ResourceDAL.create_resource(
            owner_id=owner.user_id,
            title='Test Study Room',
            description='A test study room',
            category='study_room',
            location='Library Floor 3',
            capacity=6,
            status='published',
            requires_approval=False
        )
        return resource.resource_id


class TestBookingConflictDetection:
    """Test conflict detection logic."""
    
    def test_no_conflict_different_times(self, app, sample_user, sample_resource):
        """Test that bookings at different times don't conflict."""
        with app.app_context():
            now = datetime.now()
            
            # Create first booking
            booking1 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='Study session 1'
            )
            
            # Try to create second booking at different time
            booking2 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=3),
                end_datetime=now + timedelta(hours=4),
                purpose='Study session 2'
            )
            
            assert booking1 is not None, "First booking should be created"
            assert booking2 is not None, "Second booking should be created (no conflict)"
    
    def test_conflict_overlapping_times(self, app, sample_user, sample_resource):
        """Test that overlapping bookings are detected as conflicts."""
        with app.app_context():
            now = datetime.now()
            
            # Create first booking (1 PM to 3 PM)
            booking1 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=3),
                purpose='Study session 1'
            )
            
            # Try to create overlapping booking (2 PM to 4 PM)
            booking2 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=2),
                end_datetime=now + timedelta(hours=4),
                purpose='Study session 2'
            )
            
            assert booking1 is not None, "First booking should be created"
            assert booking2 is None, "Second booking should fail due to conflict"
    
    def test_conflict_same_start_time(self, app, sample_user, sample_resource):
        """Test that bookings with same start time conflict."""
        with app.app_context():
            now = datetime.now()
            start = now + timedelta(hours=1)
            
            # Create first booking
            booking1 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=start,
                end_datetime=start + timedelta(hours=2),
                purpose='Study session 1'
            )
            
            # Try to create booking at exact same start time
            booking2 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=start,
                end_datetime=start + timedelta(hours=1),
                purpose='Study session 2'
            )
            
            assert booking1 is not None
            assert booking2 is None, "Booking with same start time should conflict"
    
    def test_conflict_contained_booking(self, app, sample_user, sample_resource):
        """Test that a booking contained within another conflicts."""
        with app.app_context():
            now = datetime.now()
            
            # Create first booking (1 PM to 5 PM)
            booking1 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=5),
                purpose='Long study session'
            )
            
            # Try to create booking contained within (2 PM to 3 PM)
            booking2 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=2),
                end_datetime=now + timedelta(hours=3),
                purpose='Short session'
            )
            
            assert booking1 is not None
            assert booking2 is None, "Contained booking should conflict"
    
    def test_no_conflict_cancelled_booking(self, app, sample_user, sample_resource):
        """Test that cancelled bookings don't cause conflicts."""
        with app.app_context():
            now = datetime.now()
            start = now + timedelta(hours=1)
            end = now + timedelta(hours=2)
            
            # Create and cancel first booking
            booking1 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=start,
                end_datetime=end,
                purpose='Cancelled session'
            )
            BookingDAL.update_booking_status(booking1.booking_id, 'cancelled')
            
            # Try to create booking at same time
            booking2 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=start,
                end_datetime=end,
                purpose='New session'
            )
            
            assert booking2 is not None, "Booking should succeed when previous is cancelled"


class TestBookingStatusTransitions:
    """Test booking status transitions."""
    
    def test_auto_approve_study_room(self, app, sample_user, sample_resource):
        """Test that study rooms are auto-approved."""
        with app.app_context():
            now = datetime.now()
            
            booking = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='Study'
            )
            
            assert booking.status == 'approved', "Study room should be auto-approved"
    
    def test_pending_approval_required_resource(self, app, sample_user):
        """Test that resources requiring approval start as pending."""
        with app.app_context():
            # Create resource that requires approval
            owner = UserDAL.create_user(
                name='Lab Owner',
                email='labowner@test.edu',
                password='password123',
                role='staff'
            )
            resource = ResourceDAL.create_resource(
                owner_id=owner.user_id,
                title='Science Lab',
                description='Chemistry lab',
                category='lab',
                location='Science Building',
                capacity=20,
                status='published',
                requires_approval=True
            )
            
            now = datetime.now()
            booking = BookingDAL.create_booking(
                resource_id=resource.resource_id,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='Lab work'
            )
            
            assert booking.status == 'pending', "Lab booking should be pending"
    
    def test_status_transition_pending_to_approved(self, app, sample_user):
        """Test transitioning booking from pending to approved."""
        with app.app_context():
            owner = UserDAL.create_user(
                name='Lab Owner',
                email='labowner@test.edu',
                password='password123',
                role='staff'
            )
            resource = ResourceDAL.create_resource(
                owner_id=owner.user_id,
                title='Science Lab',
                description='Chemistry lab',
                category='lab',
                location='Science Building',
                capacity=20,
                status='published',
                requires_approval=True
            )
            
            now = datetime.now()
            booking = BookingDAL.create_booking(
                resource_id=resource.resource_id,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='Lab work'
            )
            
            # Approve the booking
            updated = BookingDAL.update_booking_status(booking.booking_id, 'approved')
            
            assert updated is not None
            assert updated.status == 'approved', "Status should be updated to approved"
    
    def test_status_transition_pending_to_rejected(self, app, sample_user):
        """Test rejecting a pending booking."""
        with app.app_context():
            owner = UserDAL.create_user(
                name='Lab Owner',
                email='labowner@test.edu',
                password='password123',
                role='staff'
            )
            resource = ResourceDAL.create_resource(
                owner_id=owner.user_id,
                title='Science Lab',
                description='Chemistry lab',
                category='lab',
                location='Science Building',
                capacity=20,
                status='published',
                requires_approval=True
            )
            
            now = datetime.now()
            booking = BookingDAL.create_booking(
                resource_id=resource.resource_id,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='Lab work'
            )
            
            # Reject the booking
            updated = BookingDAL.update_booking_status(
                booking.booking_id, 
                'rejected',
                notes='Resource unavailable'
            )
            
            assert updated.status == 'rejected'
            assert updated.notes == 'Resource unavailable'
    
    def test_cancel_approved_booking(self, app, sample_user, sample_resource):
        """Test cancelling an approved booking."""
        with app.app_context():
            now = datetime.now()
            
            booking = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='Study'
            )
            
            # Cancel the booking
            updated = BookingDAL.update_booking_status(booking.booking_id, 'cancelled')
            
            assert updated.status == 'cancelled'


class TestBookingCRUDOperations:
    """Test CRUD operations for bookings (Data Access Layer verification)."""
    
    def test_create_booking(self, app, sample_user, sample_resource):
        """Test creating a booking."""
        with app.app_context():
            now = datetime.now()
            
            booking = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='Study session',
                notes='Need quiet space'
            )
            
            assert booking is not None
            assert booking.resource_id == sample_resource
            assert booking.requester_id == sample_user
            assert booking.purpose == 'Study session'
            assert booking.notes == 'Need quiet space'
            assert booking.status == 'approved'
    
    def test_read_booking_by_id(self, app, sample_user, sample_resource):
        """Test retrieving a booking by ID."""
        with app.app_context():
            now = datetime.now()
            
            # Create booking
            booking = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='Study'
            )
            
            # Retrieve booking
            retrieved = BookingDAL.get_booking_by_id(booking.booking_id)
            
            assert retrieved is not None
            assert retrieved.booking_id == booking.booking_id
            assert retrieved.purpose == 'Study'
    
    def test_read_bookings_by_user(self, app, sample_user, sample_resource):
        """Test retrieving all bookings for a user."""
        with app.app_context():
            now = datetime.now()
            
            # Create multiple bookings
            booking1 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='Session 1'
            )
            
            booking2 = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=3),
                end_datetime=now + timedelta(hours=4),
                purpose='Session 2'
            )
            
            # Retrieve user's bookings
            bookings = BookingDAL.get_bookings_by_user(sample_user)
            
            assert len(bookings) == 2
            assert any(b.purpose == 'Session 1' for b in bookings)
            assert any(b.purpose == 'Session 2' for b in bookings)
    
    def test_update_booking(self, app, sample_user, sample_resource):
        """Test updating a booking."""
        with app.app_context():
            now = datetime.now()
            
            # Create booking
            booking = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='Original purpose'
            )
            
            # Update booking
            updated = BookingDAL.update_booking(
                booking.booking_id,
                purpose='Updated purpose',
                notes='Added notes'
            )
            
            assert updated is not None
            assert updated.purpose == 'Updated purpose'
            assert updated.notes == 'Added notes'
    
    def test_delete_booking(self, app, sample_user, sample_resource):
        """Test deleting a booking."""
        with app.app_context():
            now = datetime.now()
            
            # Create booking
            booking = BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='To be deleted'
            )
            
            booking_id = booking.booking_id
            
            # Delete booking
            result = BookingDAL.delete_booking(booking_id)
            
            assert result is True
            assert BookingDAL.get_booking_by_id(booking_id) is None
    
    def test_get_bookings_by_resource(self, app, sample_user, sample_resource):
        """Test retrieving bookings for a specific resource."""
        with app.app_context():
            now = datetime.now()
            
            # Create bookings for the resource
            BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=1),
                end_datetime=now + timedelta(hours=2),
                purpose='Booking 1'
            )
            
            BookingDAL.create_booking(
                resource_id=sample_resource,
                requester_id=sample_user,
                start_datetime=now + timedelta(hours=3),
                end_datetime=now + timedelta(hours=4),
                purpose='Booking 2'
            )
            
            # Retrieve resource's bookings
            bookings = BookingDAL.get_bookings_by_resource(sample_resource)
            
            assert len(bookings) >= 2
            assert all(b.resource_id == sample_resource for b in bookings)
