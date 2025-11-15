# AI Contribution: Copilot generated CRUD operations following DAL pattern
# Reviewed and validated by team to ensure proper error handling

"""
Data Access Layer for Users
Encapsulates all database operations for the User model.
"""

from src.models.models import db, User
from datetime import datetime
from sqlalchemy.exc import IntegrityError


class UserDAL:
    """Data Access Layer for User operations."""
    
    @staticmethod
    def create_user(name, email, password, role='student', department=None, profile_image=None):
        """
        Create a new user with hashed password.
        
        Args:
            name (str): User's full name
            email (str): User's email address (must be unique)
            password (str): Plain text password (will be hashed)
            role (str): User role (student, staff, admin)
            department (str): User's department
            profile_image (str): Path to profile image
            
        Returns:
            User: Created user object or None if email already exists
        """
        try:
            user = User(
                name=name,
                email=email.lower(),
                role=role,
                department=department,
                profile_image=profile_image
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID."""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email address."""
        return User.query.filter_by(email=email.lower()).first()
    
    @staticmethod
    def get_all_users(role=None):
        """
        Get all users, optionally filtered by role.
        
        Args:
            role (str): Filter by role (student, staff, admin)
            
        Returns:
            list: List of User objects
        """
        query = User.query
        if role:
            query = query.filter_by(role=role)
        return query.order_by(User.created_at.desc()).all()
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """
        Update user fields.
        
        Args:
            user_id (int): User ID to update
            **kwargs: Fields to update (name, department, profile_image, etc.)
            
        Returns:
            User: Updated user object or None if not found
        """
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Update allowed fields
        allowed_fields = ['name', 'department', 'profile_image', 'role']
        for field in allowed_fields:
            if field in kwargs:
                setattr(user, field, kwargs[field])
        
        try:
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            return None
    
    @staticmethod
    def update_password(user_id, new_password):
        """
        Update user password.
        
        Args:
            user_id (int): User ID
            new_password (str): New plain text password
            
        Returns:
            bool: True if successful, False otherwise
        """
        user = User.query.get(user_id)
        if not user:
            return False
        
        user.set_password(new_password)
        try:
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def delete_user(user_id):
        """
        Delete a user.
        
        Args:
            user_id (int): User ID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        user = User.query.get(user_id)
        if not user:
            return False
        
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def update_google_tokens(user_id, access_token, refresh_token, expiry):
        """
        Update user's Google Calendar OAuth tokens.
        
        Args:
            user_id (int): User ID
            access_token (str): Google access token
            refresh_token (str): Google refresh token
            expiry (datetime): Token expiry datetime
            
        Returns:
            bool: True if successful, False otherwise
        """
        user = User.query.get(user_id)
        if not user:
            return False
        
        user.google_calendar_token = access_token
        user.google_refresh_token = refresh_token
        user.google_token_expiry = expiry
        
        try:
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def search_users(query, role=None):
        """
        Search users by name or email.
        
        Args:
            query (str): Search query
            role (str): Optional role filter
            
        Returns:
            list: List of matching users
        """
        search = f"%{query}%"
        q = User.query.filter(
            (User.name.ilike(search)) | (User.email.ilike(search))
        )
        if role:
            q = q.filter_by(role=role)
        return q.order_by(User.name).all()
