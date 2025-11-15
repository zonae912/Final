# AI Contribution: Copilot generated DAL unit tests
# Reviewed and approved by team

"""
Test suite for Data Access Layer.
Tests CRUD operations independently from Flask routes.
"""

import pytest
from datetime import datetime, timedelta
from src import create_app
from src.models.models import db
from src.data_access import UserDAL, ResourceDAL, BookingDAL, ReviewDAL


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


class TestUserDAL:
    """Test User Data Access Layer."""
    
    def test_create_user(self, app):
        """Test user creation."""
        with app.app_context():
            user = UserDAL.create_user(
                name='Test User',
                email='test@example.com',
                password='password123',
                role='student'
            )
            
            assert user is not None
            assert user.name == 'Test User'
            assert user.email == 'test@example.com'
            assert user.role == 'student'
            assert user.check_password('password123')
    
    def test_get_user_by_email(self, app):
        """Test retrieving user by email."""
        with app.app_context():
            UserDAL.create_user(
                name='Test User',
                email='test@example.com',
                password='password123',
                role='student'
            )
            
            user = UserDAL.get_user_by_email('test@example.com')
            assert user is not None
            assert user.email == 'test@example.com'
    
    def test_update_user(self, app):
        """Test user update."""
        with app.app_context():
            user = UserDAL.create_user(
                name='Test User',
                email='test@example.com',
                password='password123',
                role='student'
            )
            
            updated = UserDAL.update_user(user.user_id, name='Updated Name')
            assert updated is not None
            assert updated.name == 'Updated Name'


class TestResourceDAL:
    """Test Resource Data Access Layer."""
    
    def test_create_resource(self, app):
        """Test resource creation."""
        with app.app_context():
            # Create owner first
            owner = UserDAL.create_user(
                name='Owner',
                email='owner@example.com',
                password='password123',
                role='staff'
            )
            
            resource = ResourceDAL.create_resource(
                owner_id=owner.user_id,
                title='Test Room',
                description='A test study room',
                category='study-room',
                location='Building A',
                capacity=10,
                status='published'
            )
            
            assert resource is not None
            assert resource.title == 'Test Room'
            assert resource.category == 'study-room'
    
    def test_search_resources(self, app):
        """Test resource search."""
        with app.app_context():
            owner = UserDAL.create_user(
                name='Owner',
                email='owner@example.com',
                password='password123',
                role='staff'
            )
            
            ResourceDAL.create_resource(
                owner_id=owner.user_id,
                title='Study Room 101',
                category='study-room',
                status='published'
            )
            
            ResourceDAL.create_resource(
                owner_id=owner.user_id,
                title='Laptop Charger',
                category='equipment',
                status='published'
            )
            
            results = ResourceDAL.search_resources(keyword='Room')
            assert len(results) == 1
            assert results[0].title == 'Study Room 101'


class TestBookingDAL:
    """Test Booking Data Access Layer."""
    
    def test_create_booking(self, app):
        """Test booking creation."""
        with app.app_context():
            # Setup
            owner = UserDAL.create_user(
                name='Owner', email='owner@example.com',
                password='password123', role='staff'
            )
            requester = UserDAL.create_user(
                name='Requester', email='requester@example.com',
                password='password123', role='student'
            )
            resource = ResourceDAL.create_resource(
                owner_id=owner.user_id,
                title='Test Room',
                status='published'
            )
            
            # Create booking
            start = datetime.utcnow() + timedelta(days=1)
            end = start + timedelta(hours=2)
            
            booking = BookingDAL.create_booking(
                resource_id=resource.resource_id,
                requester_id=requester.user_id,
                start_datetime=start,
                end_datetime=end
            )
            
            assert booking is not None
            assert booking.status in ['pending', 'approved']
    
    def test_conflict_detection(self, app):
        """Test booking conflict detection."""
        with app.app_context():
            # Setup
            owner = UserDAL.create_user(
                name='Owner', email='owner@example.com',
                password='password123', role='staff'
            )
            requester = UserDAL.create_user(
                name='Requester', email='requester@example.com',
                password='password123', role='student'
            )
            resource = ResourceDAL.create_resource(
                owner_id=owner.user_id,
                title='Test Room',
                status='published'
            )
            
            # Create first booking
            start1 = datetime.utcnow() + timedelta(days=1)
            end1 = start1 + timedelta(hours=2)
            
            booking1 = BookingDAL.create_booking(
                resource_id=resource.resource_id,
                requester_id=requester.user_id,
                start_datetime=start1,
                end_datetime=end1
            )
            
            # Try overlapping booking
            start2 = start1 + timedelta(hours=1)
            end2 = start2 + timedelta(hours=2)
            
            booking2 = BookingDAL.create_booking(
                resource_id=resource.resource_id,
                requester_id=requester.user_id,
                start_datetime=start2,
                end_datetime=end2
            )
            
            assert booking2 is None  # Should be rejected due to conflict


class TestReviewDAL:
    """Test Review Data Access Layer."""
    
    def test_create_review(self, app):
        """Test review creation."""
        with app.app_context():
            owner = UserDAL.create_user(
                name='Owner', email='owner@example.com',
                password='password123', role='staff'
            )
            reviewer = UserDAL.create_user(
                name='Reviewer', email='reviewer@example.com',
                password='password123', role='student'
            )
            resource = ResourceDAL.create_resource(
                owner_id=owner.user_id,
                title='Test Room',
                status='published'
            )
            
            review = ReviewDAL.create_review(
                resource_id=resource.resource_id,
                reviewer_id=reviewer.user_id,
                rating=5,
                comment='Excellent resource!'
            )
            
            assert review is not None
            assert review.rating == 5
    
    def test_average_rating(self, app):
        """Test average rating calculation."""
        with app.app_context():
            owner = UserDAL.create_user(
                name='Owner', email='owner@example.com',
                password='password123', role='staff'
            )
            resource = ResourceDAL.create_resource(
                owner_id=owner.user_id,
                title='Test Room',
                status='published'
            )
            
            # Create multiple reviews
            for i in range(3):
                reviewer = UserDAL.create_user(
                    name=f'Reviewer {i}',
                    email=f'reviewer{i}@example.com',
                    password='password123',
                    role='student'
                )
                ReviewDAL.create_review(
                    resource_id=resource.resource_id,
                    reviewer_id=reviewer.user_id,
                    rating=i + 3  # Ratings: 3, 4, 5
                )
            
            avg = ReviewDAL.get_average_rating(resource.resource_id)
            assert avg == 4.0  # (3+4+5)/3
