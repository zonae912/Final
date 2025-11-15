# AI Contribution: Copilot generated pytest test suite for authentication
# Reviewed and validated by team

"""
Test suite for authentication functionality.
Tests user registration, login, logout, and profile management.
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


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


def test_registration(client):
    """Test user registration."""
    response = client.post('/auth/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'student',
        'department': 'Computer Science'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Registration successful' in response.data or b'Login' in response.data


def test_login(client, app):
    """Test user login."""
    # Create test user
    with app.app_context():
        UserDAL.create_user(
            name='Test User',
            email='test@example.com',
            password='password123',
            role='student'
        )
    
    # Test login
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Welcome' in response.data or b'Dashboard' in response.data


def test_logout(client, app):
    """Test user logout."""
    # Create and login user
    with app.app_context():
        UserDAL.create_user(
            name='Test User',
            email='test@example.com',
            password='password123',
            role='student'
        )
    
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Test logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'logged out' in response.data.lower()


def test_invalid_login(client):
    """Test login with invalid credentials."""
    response = client.post('/auth/login', data={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid' in response.data or b'incorrect' in response.data.lower()


def test_duplicate_registration(client, app):
    """Test registration with duplicate email."""
    with app.app_context():
        UserDAL.create_user(
            name='Test User',
            email='test@example.com',
            password='password123',
            role='student'
        )
    
    response = client.post('/auth/register', data={
        'name': 'Another User',
        'email': 'test@example.com',
        'password': 'password456',
        'confirm_password': 'password456',
        'role': 'student'
    }, follow_redirects=True)
    
    assert b'already registered' in response.data.lower() or b'exists' in response.data.lower()
