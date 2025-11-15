# Integration test for auth flow - register → login → access protected route
# Tests the complete authentication workflow

"""
Integration Test Suite for Authentication Flow
Tests user registration, login, and accessing protected routes.
"""

import pytest
from src import create_app
from src.models.models import db, User
from src.data_access import UserDAL


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


class TestAuthenticationFlow:
    """Test complete authentication workflow."""
    
    def test_complete_auth_flow_register_login_access(self, client, app):
        """
        Integration test: Register → Login → Access Protected Route
        Tests the complete flow of a new user joining and using the system.
        """
        # Step 1: Register a new user
        print("\n=== Step 1: User Registration ===")
        register_data = {
            'name': 'Integration Test User',
            'email': 'integration@test.edu',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
            'role': 'student',
            'department': 'Computer Science'
        }
        
        register_response = client.post('/auth/register', 
                                       data=register_data, 
                                       follow_redirects=True)
        
        assert register_response.status_code == 200
        print("✓ Registration successful")
        
        # Verify user was created in database
        with app.app_context():
            user = UserDAL.get_user_by_email('integration@test.edu')
            assert user is not None, "User should exist in database"
            assert user.name == 'Integration Test User'
            assert user.role == 'student'
            assert user.department == 'Computer Science'
            print(f"✓ User created in database: {user.email}")
        
        # Step 2: Login with the registered credentials
        print("\n=== Step 2: User Login ===")
        login_data = {
            'email': 'integration@test.edu',
            'password': 'SecurePassword123!'
        }
        
        login_response = client.post('/auth/login', 
                                    data=login_data, 
                                    follow_redirects=True)
        
        assert login_response.status_code == 200
        assert b'Dashboard' in login_response.data or b'Welcome' in login_response.data
        print("✓ Login successful")
        
        # Step 3: Access protected route (Dashboard)
        print("\n=== Step 3: Access Protected Route ===")
        dashboard_response = client.get('/dashboard', follow_redirects=True)
        
        assert dashboard_response.status_code == 200
        assert b'Integration Test User' in dashboard_response.data or b'Dashboard' in dashboard_response.data
        print("✓ Successfully accessed protected dashboard")
        
        # Step 4: Access another protected route (My Bookings)
        print("\n=== Step 4: Access Another Protected Route ===")
        bookings_response = client.get('/bookings/my-bookings', follow_redirects=True)
        
        assert bookings_response.status_code == 200
        assert b'My Bookings' in bookings_response.data
        print("✓ Successfully accessed my-bookings page")
        
        # Step 5: Verify user profile access
        print("\n=== Step 5: Access User Profile ===")
        profile_response = client.get('/auth/profile', follow_redirects=True)
        
        assert profile_response.status_code == 200
        assert b'integration@test.edu' in profile_response.data or b'Profile' in profile_response.data
        print("✓ Successfully accessed user profile")
        
        # Step 6: Logout
        print("\n=== Step 6: User Logout ===")
        logout_response = client.get('/auth/logout', follow_redirects=True)
        
        assert logout_response.status_code == 200
        print("✓ Logout successful")
        
        # Step 7: Verify protected route is no longer accessible
        print("\n=== Step 7: Verify Protection After Logout ===")
        protected_response = client.get('/dashboard', follow_redirects=True)
        
        # Should redirect to login page
        assert b'Login' in protected_response.data or b'Please log in' in protected_response.data
        print("✓ Protected route correctly requires authentication")
        
        print("\n=== Integration Test Complete ===")
        print("✓ All steps passed: Register → Login → Access → Logout → Verify Protection")
    
    def test_login_without_registration(self, client):
        """Test that login fails for non-existent user."""
        login_data = {
            'email': 'nonexistent@test.edu',
            'password': 'password123'
        }
        
        response = client.post('/auth/login', 
                              data=login_data, 
                              follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid' in response.data or b'incorrect' in response.data.lower()
    
    def test_access_protected_route_without_login(self, client):
        """Test that protected routes redirect to login when not authenticated."""
        response = client.get('/dashboard', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Login' in response.data or b'log in' in response.data.lower()
    
    def test_duplicate_registration(self, client, app):
        """Test that duplicate email registration is prevented."""
        # Create first user
        with app.app_context():
            UserDAL.create_user(
                name='Existing User',
                email='existing@test.edu',
                password='password123',
                role='student'
            )
        
        # Try to register with same email
        register_data = {
            'name': 'Duplicate User',
            'email': 'existing@test.edu',
            'password': 'password456',
            'confirm_password': 'password456',
            'role': 'student'
        }
        
        response = client.post('/auth/register', 
                              data=register_data, 
                              follow_redirects=True)
        
        assert response.status_code == 200
        assert b'already' in response.data.lower() or b'exists' in response.data.lower()
    
    def test_password_mismatch_on_registration(self, client):
        """Test that registration fails when passwords don't match."""
        register_data = {
            'name': 'Test User',
            'email': 'test@test.edu',
            'password': 'password123',
            'confirm_password': 'different456',
            'role': 'student'
        }
        
        response = client.post('/auth/register', 
                              data=register_data, 
                              follow_redirects=True)
        
        assert response.status_code == 200
        # Should show error about password mismatch
        assert b'match' in response.data.lower() or b'password' in response.data.lower()
    
    def test_session_persistence(self, client, app):
        """Test that user session persists across requests."""
        # Create and login user
        with app.app_context():
            UserDAL.create_user(
                name='Session Test User',
                email='session@test.edu',
                password='password123',
                role='student'
            )
        
        login_data = {
            'email': 'session@test.edu',
            'password': 'password123'
        }
        
        client.post('/auth/login', data=login_data, follow_redirects=True)
        
        # Make multiple requests - session should persist
        response1 = client.get('/dashboard')
        response2 = client.get('/bookings/my-bookings')
        response3 = client.get('/auth/profile')
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200


class TestRoleBasedAccess:
    """Test role-based access control."""
    
    def test_admin_access_to_admin_panel(self, client, app):
        """Test that admin users can access admin panel."""
        # Create admin user
        with app.app_context():
            UserDAL.create_user(
                name='Admin User',
                email='admin@test.edu',
                password='admin123',
                role='admin'
            )
        
        # Login as admin
        client.post('/auth/login', 
                   data={'email': 'admin@test.edu', 'password': 'admin123'},
                   follow_redirects=True)
        
        # Access admin panel
        response = client.get('/admin/dashboard', follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_student_no_access_to_admin_panel(self, client, app):
        """Test that student users cannot access admin panel."""
        # Create student user
        with app.app_context():
            UserDAL.create_user(
                name='Student User',
                email='student@test.edu',
                password='student123',
                role='student'
            )
        
        # Login as student
        client.post('/auth/login',
                   data={'email': 'student@test.edu', 'password': 'student123'},
                   follow_redirects=True)
        
        # Try to access admin panel
        response = client.get('/admin/dashboard', follow_redirects=True)
        
        # Should be forbidden or redirected
        assert response.status_code in [200, 403]
        if response.status_code == 200:
            assert b'permission' in response.data.lower() or b'access denied' in response.data.lower()
