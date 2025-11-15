# AI Contribution: Copilot Agent structured the configuration following Flask best practices
# Reviewed and approved by team

import os
from datetime import timedelta

class Config:
    """Base configuration class for the Campus Resource Hub application."""
    
    # Flask core settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'campus_hub.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # CSRF tokens don't expire
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src', 'static', 'uploads')
    
    # Gemini AI Chatbot settings
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'AIzaSyDpGGhCK_qaGWTEAMz2FGym6sjk6WPlDkc'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # Google API settings
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    GOOGLE_CSE_API_KEY = os.environ.get('GOOGLE_CSE_API_KEY')
    GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')
    
    # OAuth settings
    OAUTHLIB_INSECURE_TRANSPORT = os.environ.get('FLASK_ENV') != 'production'  # Allow HTTP for dev
    
    # Pagination settings
    RESOURCES_PER_PAGE = 12
    BOOKINGS_PER_PAGE = 20
    MESSAGES_PER_PAGE = 30
    
    # Email settings (for notifications)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@campushub.edu')
    
    # Application settings
    APP_NAME = "Campus Resource Hub"
    APP_VERSION = "1.0.0"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
