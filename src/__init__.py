# AI Contribution: Copilot structured Flask application factory pattern
# Reviewed and enhanced by team for security and modular design

"""
Flask Application Factory for Campus Resource Hub
"""

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os

from src.models.models import db, User
from config import config


def create_app(config_name='default'):
    """
    Create and configure the Flask application.
    
    Args:
        config_name (str): Configuration name (development, testing, production)
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__, 
                template_folder='views',
                static_folder='static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login."""
        return User.query.get(int(user_id))
    
    # Register blueprints
    from src.controllers.auth_controller import auth_bp
    from src.controllers.main_controller import main_bp
    from src.controllers.resource_controller import resource_bp
    from src.controllers.booking_controller import booking_bp
    from src.controllers.message_controller import message_bp
    from src.controllers.review_controller import review_bp
    from src.controllers.admin_controller import admin_bp
    from src.controllers.calendar_controller import calendar_bp
    from src.controllers.chatbot_controller import chatbot_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(resource_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(chatbot_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register template filters
    register_template_filters(app)
    
    # Register context processors
    register_context_processors(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app


def register_context_processors(app):
    """Register context processors to inject variables into all templates."""
    from datetime import datetime
    
    @app.context_processor
    def inject_now():
        """Make 'now' function available in all templates."""
        return {'now': datetime.now}


def register_template_filters(app):
    """Register custom Jinja2 template filters."""
    
    @app.template_filter('from_json')
    def from_json(value):
        """Parse JSON string to Python object."""
        if not value:
            return []
        import json
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []
    
    @app.template_filter('datetime_format')
    def datetime_format(value, format='%Y-%m-%d %H:%M'):
        """Format datetime for display."""
        if value is None:
            return ''
        return value.strftime(format)
    
    @app.template_filter('date_format')
    def date_format(value, format='%Y-%m-%d'):
        """Format date for display."""
        if value is None:
            return ''
        return value.strftime(format)
    
    @app.template_filter('time_ago')
    def time_ago(value):
        """Convert datetime to 'time ago' string."""
        if value is None:
            return ''
        
        from datetime import datetime
        now = datetime.utcnow()
        diff = now - value
        
        if diff.days > 365:
            return f"{diff.days // 365} year{'s' if diff.days // 365 > 1 else ''} ago"
        elif diff.days > 30:
            return f"{diff.days // 30} month{'s' if diff.days // 30 > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hour{'s' if diff.seconds // 3600 > 1 else ''} ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minute{'s' if diff.seconds // 60 > 1 else ''} ago"
        else:
            return "just now"
    
    # Register timeago as an alias for time_ago
    app.jinja_env.filters['timeago'] = time_ago
    
    @app.template_filter('star_rating')
    def star_rating(rating):
        """Convert numeric rating to star HTML."""
        if rating is None:
            rating = 0
        
        full_stars = int(rating)
        half_star = 1 if (rating - full_stars) >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        
        html = ''
        # Full stars
        for _ in range(full_stars):
            html += '<i class="bi bi-star-fill text-warning"></i>'
        # Half star
        if half_star:
            html += '<i class="bi bi-star-half text-warning"></i>'
        # Empty stars
        for _ in range(empty_stars):
            html += '<i class="bi bi-star text-warning"></i>'
        
        return html
    
    @app.template_filter('rating_badge')
    def rating_badge_filter(resource_id):
        """Get rating badge for a resource."""
        from src.data_access import ResourceDAL
        return ResourceDAL.get_resource_rating_badge(resource_id)


def register_error_handlers(app):
    """Register error handlers for common HTTP errors."""
    
    from flask import render_template
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
