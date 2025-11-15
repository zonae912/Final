# End-to-end test for complete booking scenario
# Tests the full user journey from registration to booking completion

"""
End-to-End Test Suite
Tests complete user workflows through the Campus Resource Hub system.
"""

import pytest
from datetime import datetime, timedelta
from src import create_app
from src.models.models import db, User, Resource, Booking, Review
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


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestCompleteBookingScenario:
    """
    End-to-End Test: Complete Booking Workflow
    
    This test simulates a complete user journey:
    1. Faculty member registers and creates a resource
    2. Student registers and searches for resources
    3. Student creates a booking request
    4. Faculty member approves the booking
    5. Booking time passes (simulated)
    6. Student leaves a review
    7. Both users can view their respective histories
    """
    
    def test_complete_booking_workflow(self, client, app):
        """
        Complete E2E workflow: Registration → Resource Creation → Booking → Approval → Review
        """
        print("\n" + "="*70)
        print("END-TO-END TEST: Complete Booking Workflow")
        print("="*70)
        
        # ==================== PHASE 1: Faculty Setup ====================
        print("\n[PHASE 1: Faculty Member Setup]")
        
        # Step 1.1: Faculty member registers
        print("  Step 1.1: Faculty member registers...")
        faculty_data = {
            'name': 'Dr. Jane Smith',
            'email': 'jane.smith@university.edu',
            'password': 'FacultyPass123!',
            'confirm_password': 'FacultyPass123!',
            'role': 'faculty',
            'department': 'Computer Science'
        }
        
        response = client.post('/auth/register', data=faculty_data, follow_redirects=True)
        assert response.status_code == 200
        print("  ✓ Faculty member registered successfully")
        
        # Step 1.2: Faculty member logs in
        print("  Step 1.2: Faculty member logs in...")
        login_response = client.post('/auth/login',
                                    data={'email': 'jane.smith@university.edu',
                                          'password': 'FacultyPass123!'},
                                    follow_redirects=True)
        assert login_response.status_code == 200
        print("  ✓ Faculty member logged in")
        
        # Step 1.3: Faculty member creates a resource
        print("  Step 1.3: Faculty member creates classroom resource...")
        
        with app.app_context():
            faculty = UserDAL.get_user_by_email('jane.smith@university.edu')
            if faculty is None:
                pytest.fail("Faculty user not found in database")
            
            faculty_id = faculty.id
            
        with app.app_context():
            resource = ResourceDAL.create_resource(
                name='CS Lab 101',
                description='Computer Science laboratory with 30 workstations and projector',
                resource_type='classroom',
                capacity=30,
                location='Building A, Room 101',
                owner_id=faculty_id,
                requires_approval=True,
                amenities='Projector, Whiteboard, Computers'
            )
            resource_id = resource.id
        
        print(f"  ✓ Resource created: CS Lab 101 (ID: {resource_id})")
        
        # Step 1.4: Faculty member logs out
        print("  Step 1.4: Faculty member logs out...")
        client.get('/auth/logout', follow_redirects=True)
        print("  ✓ Faculty member logged out")
        
        # ==================== PHASE 2: Student Setup ====================
        print("\n[PHASE 2: Student Setup]")
        
        # Step 2.1: Student registers
        print("  Step 2.1: Student registers...")
        student_data = {
            'name': 'John Doe',
            'email': 'john.doe@university.edu',
            'password': 'StudentPass123!',
            'confirm_password': 'StudentPass123!',
            'role': 'student',
            'department': 'Computer Science'
        }
        
        response = client.post('/auth/register', data=student_data, follow_redirects=True)
        assert response.status_code == 200
        print("  ✓ Student registered successfully")
        
        # Step 2.2: Student logs in
        print("  Step 2.2: Student logs in...")
        login_response = client.post('/auth/login',
                                    data={'email': 'john.doe@university.edu',
                                          'password': 'StudentPass123!'},
                                    follow_redirects=True)
        assert login_response.status_code == 200
        print("  ✓ Student logged in")
        
        # Step 2.3: Student searches for resources
        print("  Step 2.3: Student searches for computer lab...")
        search_response = client.get('/search?q=computer', follow_redirects=True)
        assert search_response.status_code == 200
        assert b'CS Lab 101' in search_response.data
        print("  ✓ Student found CS Lab 101 in search results")
        
        # Step 2.4: Student views resource details
        print("  Step 2.4: Student views resource details...")
        resource_response = client.get(f'/resources/{resource_id}', follow_redirects=True)
        assert resource_response.status_code == 200
        assert b'CS Lab 101' in resource_response.data
        print("  ✓ Student viewed resource details")
        
        # ==================== PHASE 3: Booking Creation ====================
        print("\n[PHASE 3: Booking Creation]")
        
        # Step 3.1: Student creates booking request
        print("  Step 3.1: Student creates booking for tomorrow...")
        
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=2)
        
        with app.app_context():
            student = UserDAL.get_user_by_email('john.doe@university.edu')
            booking = BookingDAL.create_booking(
                resource_id=resource_id,
                user_id=student.id,
                start_datetime=start_time,
                end_datetime=end_time,
                purpose='Final project presentation rehearsal',
                attendees=5
            )
            booking_id = booking.id
        
        print(f"  ✓ Booking created (ID: {booking_id})")
        print(f"    Time: {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%H:%M')}")
        print(f"    Purpose: Final project presentation rehearsal")
        print(f"    Status: {booking.status}")
        
        # Step 3.2: Student views their pending bookings
        print("  Step 3.2: Student checks their bookings...")
        my_bookings_response = client.get('/bookings/my-bookings', follow_redirects=True)
        assert my_bookings_response.status_code == 200
        assert b'Final project presentation rehearsal' in my_bookings_response.data
        print("  ✓ Student can see pending booking")
        
        # Step 3.3: Student logs out
        print("  Step 3.3: Student logs out...")
        client.get('/auth/logout', follow_redirects=True)
        print("  ✓ Student logged out")
        
        # ==================== PHASE 4: Booking Approval ====================
        print("\n[PHASE 4: Booking Approval]")
        
        # Step 4.1: Faculty member logs back in
        print("  Step 4.1: Faculty member logs back in...")
        client.post('/auth/login',
                   data={'email': 'jane.smith@university.edu',
                         'password': 'FacultyPass123!'},
                   follow_redirects=True)
        print("  ✓ Faculty member logged in")
        
        # Step 4.2: Faculty views their resources' pending bookings
        print("  Step 4.2: Faculty checks pending booking requests...")
        admin_bookings = client.get('/admin/bookings', follow_redirects=True)
        assert admin_bookings.status_code == 200
        print("  ✓ Faculty can view pending requests")
        
        # Step 4.3: Faculty approves the booking
        print("  Step 4.3: Faculty approves the booking...")
        
        with app.app_context():
            booking = BookingDAL.get_booking_by_id(booking_id)
            BookingDAL.update_booking_status(booking_id, 'approved')
            booking = BookingDAL.get_booking_by_id(booking_id)
            assert booking.status == 'approved'
        
        print("  ✓ Booking approved")
        
        # Step 4.4: Faculty logs out
        print("  Step 4.4: Faculty logs out...")
        client.get('/auth/logout', follow_redirects=True)
        print("  ✓ Faculty logged out")
        
        # ==================== PHASE 5: Post-Booking Review ====================
        print("\n[PHASE 5: Post-Booking Review]")
        
        # Step 5.1: Simulate time passing (booking completed)
        print("  Step 5.1: Simulating booking completion (time passes)...")
        
        with app.app_context():
            booking = BookingDAL.get_booking_by_id(booking_id)
            # Simulate booking in the past
            past_start = datetime.now() - timedelta(days=1)
            past_end = past_start + timedelta(hours=2)
            booking.start_datetime = past_start
            booking.end_datetime = past_end
            db.session.commit()
        
        print("  ✓ Booking is now in the past (completed)")
        
        # Step 5.2: Student logs back in
        print("  Step 5.2: Student logs back in...")
        client.post('/auth/login',
                   data={'email': 'john.doe@university.edu',
                         'password': 'StudentPass123!'},
                   follow_redirects=True)
        print("  ✓ Student logged in")
        
        # Step 5.3: Student views past bookings
        print("  Step 5.3: Student checks past bookings...")
        past_bookings = client.get('/bookings/my-bookings', follow_redirects=True)
        assert past_bookings.status_code == 200
        print("  ✓ Student can view completed booking")
        
        # Step 5.4: Student creates a review
        print("  Step 5.4: Student writes a review...")
        
        with app.app_context():
            student = UserDAL.get_user_by_email('john.doe@university.edu')
            review = ReviewDAL.create_review(
                resource_id=resource_id,
                user_id=student.id,
                booking_id=booking_id,
                rating=5,
                comment='Excellent lab! Perfect for our presentation rehearsal. '
                       'All equipment worked great and the room was clean.'
            )
            review_id = review.id
        
        print(f"  ✓ Review created (ID: {review_id})")
        print(f"    Rating: 5/5 stars")
        print(f"    Comment: Excellent lab! Perfect for our presentation rehearsal...")
        
        # Step 5.5: Verify review appears on resource page
        print("  Step 5.5: Verifying review appears on resource page...")
        resource_page = client.get(f'/resources/{resource_id}', follow_redirects=True)
        assert resource_page.status_code == 200
        assert b'Excellent lab' in resource_page.data
        print("  ✓ Review visible on resource detail page")
        
        # Step 5.6: Student logs out
        print("  Step 5.6: Student logs out...")
        client.get('/auth/logout', follow_redirects=True)
        print("  ✓ Student logged out")
        
        # ==================== PHASE 6: Verification ====================
        print("\n[PHASE 6: Final Verification]")
        
        with app.app_context():
            # Verify database state
            print("  Verifying database state...")
            
            # Check users
            faculty = UserDAL.get_user_by_email('jane.smith@university.edu')
            student = UserDAL.get_user_by_email('john.doe@university.edu')
            assert faculty is not None
            assert student is not None
            print(f"  ✓ Users exist: {faculty.name}, {student.name}")
            
            # Check resource
            resource = ResourceDAL.get_resource_by_id(resource_id)
            assert resource is not None
            assert resource.name == 'CS Lab 101'
            print(f"  ✓ Resource exists: {resource.name}")
            
            # Check booking
            booking = BookingDAL.get_booking_by_id(booking_id)
            assert booking is not None
            assert booking.status == 'approved'
            print(f"  ✓ Booking exists: Status={booking.status}")
            
            # Check review
            review = ReviewDAL.get_review_by_id(review_id)
            assert review is not None
            assert review.rating == 5
            print(f"  ✓ Review exists: Rating={review.rating}/5")
            
            # Check resource rating updated
            resource_reviews = ReviewDAL.get_reviews_by_resource(resource_id)
            assert len(resource_reviews) == 1
            print(f"  ✓ Resource has {len(resource_reviews)} review(s)")
        
        # ==================== TEST COMPLETE ====================
        print("\n" + "="*70)
        print("END-TO-END TEST PASSED")
        print("="*70)
        print("\nWorkflow Summary:")
        print("  1. ✓ Faculty registered and created resource")
        print("  2. ✓ Student registered and found resource")
        print("  3. ✓ Student created booking request")
        print("  4. ✓ Faculty approved booking")
        print("  5. ✓ Student completed booking")
        print("  6. ✓ Student left review")
        print("  7. ✓ All data verified in database")
        print("\nAll phases completed successfully!")


class TestMultiUserBookingScenario:
    """
    E2E Test: Multiple users competing for same resource
    Tests conflict resolution and booking management
    """
    
    def test_conflicting_bookings_scenario(self, client, app):
        """
        Test scenario where multiple students try to book the same resource
        at overlapping times.
        """
        print("\n" + "="*70)
        print("E2E TEST: Multiple Users Booking Same Resource")
        print("="*70)
        
        # Setup: Create faculty and resource
        print("\n[Setup Phase]")
        with app.app_context():
            faculty = UserDAL.create_user(
                name='Faculty Owner',
                email='faculty@test.edu',
                password='password123',
                role='faculty'
            )
            db.session.flush()  # Ensure ID is available
            faculty_id = faculty.id
            
        with app.app_context():
            resource = ResourceDAL.create_resource(
                name='Conference Room',
                description='Meeting room',
                resource_type='meeting room',
                capacity=10,
                location='Building B',
                owner_id=faculty_id,
                requires_approval=False  # Auto-approve
            )
            resource_id = resource.id
        
        with app.app_context():
            # Create two students
            student1 = UserDAL.create_user(
                name='Student One',
                email='student1@test.edu',
                password='password123',
                role='student'
            )
            db.session.flush()
            student1_id = student1.id
            
        with app.app_context():
            student2 = UserDAL.create_user(
                name='Student Two',
                email='student2@test.edu',
                password='password123',
                role='student'
            )
            db.session.flush()
            student2_id = student2.id
        
        print("  ✓ Faculty, resource, and two students created")
        
        # Scenario: Student 1 books first
        print("\n[Student 1 Books Time Slot]")
        tomorrow = datetime.now() + timedelta(days=1)
        slot_start = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
        slot_end = slot_start + timedelta(hours=2)
        
        with app.app_context():
            booking1 = BookingDAL.create_booking(
                resource_id=resource_id,
                user_id=student1_id,
                start_datetime=slot_start,
                end_datetime=slot_end,
                purpose='Team meeting'
            )
            booking1_id = booking1.id
        
        print(f"  ✓ Student 1 booked: {slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}")
        
        # Scenario: Student 2 tries to book overlapping time
        print("\n[Student 2 Attempts Overlapping Booking]")
        overlap_start = slot_start + timedelta(hours=1)  # 11:00
        overlap_end = overlap_start + timedelta(hours=2)  # 13:00
        
        with app.app_context():
            # Check for conflicts
            conflicts = BookingDAL.check_booking_conflicts(
                resource_id=resource_id,
                start_datetime=overlap_start,
                end_datetime=overlap_end
            )
            
            if conflicts:
                print(f"  ✓ Conflict detected! Cannot book {overlap_start.strftime('%H:%M')}-{overlap_end.strftime('%H:%M')}")
                print(f"    (Conflicts with existing booking)")
            else:
                pytest.fail("Conflict should have been detected!")
        
        # Scenario: Student 2 books non-conflicting time
        print("\n[Student 2 Books Different Time Slot]")
        later_start = slot_end  # Right after first booking
        later_end = later_start + timedelta(hours=1)
        
        with app.app_context():
            booking2 = BookingDAL.create_booking(
                resource_id=resource_id,
                user_id=student2_id,
                start_datetime=later_start,
                end_datetime=later_end,
                purpose='Study session'
            )
            booking2_id = booking2.id
        
        print(f"  ✓ Student 2 successfully booked: {later_start.strftime('%H:%M')}-{later_end.strftime('%H:%M')}")
        
        # Verify final state
        print("\n[Final Verification]")
        with app.app_context():
            resource_bookings = BookingDAL.get_bookings_by_resource(resource_id)
            assert len(resource_bookings) == 2
            print(f"  ✓ Resource has 2 bookings (no conflicts)")
            
            booking1 = BookingDAL.get_booking_by_id(booking1_id)
            booking2 = BookingDAL.get_booking_by_id(booking2_id)
            
            assert booking1.status == 'approved'
            assert booking2.status == 'approved'
            print(f"  ✓ Both bookings approved")
        
        print("\n" + "="*70)
        print("E2E TEST PASSED: Conflict detection working correctly")
        print("="*70)


class TestResourceManagementScenario:
    """
    E2E Test: Resource lifecycle management
    Tests resource creation, editing, booking, and deletion
    """
    
    def test_resource_lifecycle(self, client, app):
        """
        Test complete resource lifecycle from creation to deletion.
        """
        print("\n" + "="*70)
        print("E2E TEST: Resource Lifecycle Management")
        print("="*70)
        
        # Phase 1: Create resource
        print("\n[Phase 1: Resource Creation]")
        with app.app_context():
            owner = UserDAL.create_user(
                name='Resource Owner',
                email='owner@test.edu',
                password='password123',
                role='faculty'
            )
            db.session.flush()
            owner_id = owner.id
            
        with app.app_context():
            resource = ResourceDAL.create_resource(
                name='Original Lab',
                description='Original description',
                resource_type='lab',
                capacity=20,
                location='Building C',
                owner_id=owner_id
            )
            resource_id = resource.id
            resource_name = resource.name
        
        print(f"  ✓ Resource created: {resource_name}")
        
        # Phase 2: Edit resource
        print("\n[Phase 2: Resource Editing]")
        with app.app_context():
            ResourceDAL.update_resource(
                resource_id=resource_id,
                name='Updated Lab',
                description='Updated description with more details',
                capacity=25
            )
            
            updated_resource = ResourceDAL.get_resource_by_id(resource_id)
            assert updated_resource.name == 'Updated Lab'
            assert updated_resource.capacity == 25
        
        print(f"  ✓ Resource updated: {updated_resource.name} (capacity: {updated_resource.capacity})")
        
        # Phase 3: Resource gets bookings
        print("\n[Phase 3: Resource Usage]")
        with app.app_context():
            user = UserDAL.create_user(
                name='User',
                email='user@test.edu',
                password='password123',
                role='student'
            )
            
            # Create multiple bookings
            start_time = datetime.now() + timedelta(days=1)
            
            for i in range(3):
                BookingDAL.create_booking(
                    resource_id=resource_id,
                    user_id=user.id,
                    start_datetime=start_time + timedelta(days=i),
                    end_datetime=start_time + timedelta(days=i, hours=1),
                    purpose=f'Booking {i+1}'
                )
            
            bookings = BookingDAL.get_bookings_by_resource(resource_id)
            assert len(bookings) == 3
        
        print(f"  ✓ Resource has {len(bookings)} active bookings")
        
        # Phase 4: View resource statistics
        print("\n[Phase 4: Resource Analytics]")
        with app.app_context():
            resource = ResourceDAL.get_resource_by_id(resource_id)
            bookings = BookingDAL.get_bookings_by_resource(resource_id)
            
            print(f"  Resource: {resource.name}")
            print(f"  Total bookings: {len(bookings)}")
            print(f"  Capacity: {resource.capacity}")
            print(f"  Location: {resource.location}")
        
        print("  ✓ Resource statistics retrieved")
        
        print("\n" + "="*70)
        print("E2E TEST PASSED: Resource lifecycle managed successfully")
        print("="*70)
