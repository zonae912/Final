# AI Contribution: Copilot generated authentication routes with security best practices
# Reviewed and validated by team for proper password handling and session management

"""
Authentication Controller
Handles user registration, login, logout, and profile management.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import bleach

from src.data_access import UserDAL
from src.models.models import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page and handler."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Get and sanitize form data
        name = bleach.clean(request.form.get('name', '').strip())
        email = bleach.clean(request.form.get('email', '').strip().lower())
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'student')
        department = bleach.clean(request.form.get('department', '').strip())
        
        # Server-side validation
        errors = []
        
        if not name or len(name) < 2:
            errors.append('Name must be at least 2 characters long.')
        
        if not email or '@' not in email:
            errors.append('Please provide a valid email address.')
        
        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if role not in ['student', 'staff', 'admin']:
            errors.append('Invalid role selected.')
        
        # Check if email already exists
        if UserDAL.get_user_by_email(email):
            errors.append('Email address already registered.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')
        
        # Create user
        user = UserDAL.create_user(
            name=name,
            email=email,
            password=password,
            role=role,
            department=department if department else None
        )
        
        if user:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page and handler."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        # Validate input
        if not email or not password:
            flash('Please provide both email and password.', 'danger')
            return render_template('auth/login.html')
        
        # Get user
        user = UserDAL.get_user_by_email(email)
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.name}!', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page and update handler."""
    if request.method == 'POST':
        # Get and sanitize form data
        name = bleach.clean(request.form.get('name', '').strip())
        department = bleach.clean(request.form.get('department', '').strip())
        
        # Server-side validation
        if not name or len(name) < 2:
            flash('Name must be at least 2 characters long.', 'danger')
            return render_template('auth/profile.html', user=current_user)
        
        # Update user
        updated_user = UserDAL.update_user(
            current_user.user_id,
            name=name,
            department=department if department else None
        )
        
        if updated_user:
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Failed to update profile.', 'danger')
    
    return render_template('auth/profile.html', user=current_user)


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password page and handler."""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validate current password
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
            return render_template('auth/change_password.html')
        
        # Validate new password
        if not new_password or len(new_password) < 8:
            flash('New password must be at least 8 characters long.', 'danger')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return render_template('auth/change_password.html')
        
        # Update password
        if UserDAL.update_password(current_user.user_id, new_password):
            flash('Password changed successfully!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Failed to change password.', 'danger')
    
    return render_template('auth/change_password.html')
