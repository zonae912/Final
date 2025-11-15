# AI Contribution: Copilot suggested SQLAlchemy model structure based on project schema
# Reviewed and modified by team to include all required fields and relationships

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model representing students, staff, and administrators."""
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # student, staff, admin
    profile_image = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # OAuth fields for Google Calendar integration
    google_calendar_token = db.Column(db.Text, nullable=True)
    google_refresh_token = db.Column(db.Text, nullable=True)
    google_token_expiry = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    resources_owned = db.relationship('Resource', backref='owner', lazy='dynamic', 
                                     foreign_keys='Resource.owner_id')
    bookings_made = db.relationship('Booking', backref='requester', lazy='dynamic',
                                   foreign_keys='Booking.requester_id')
    messages_sent = db.relationship('Message', backref='sender', lazy='dynamic',
                                   foreign_keys='Message.sender_id')
    messages_received = db.relationship('Message', backref='receiver', lazy='dynamic',
                                       foreign_keys='Message.receiver_id')
    reviews_written = db.relationship('Review', backref='reviewer', lazy='dynamic')
    admin_actions = db.relationship('AdminLog', backref='admin', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        """Return the user ID as a string for Flask-Login."""
        return str(self.user_id)
    
    def is_admin(self):
        """Check if user has admin privileges."""
        return self.role == 'admin'
    
    def is_staff(self):
        """Check if user has staff privileges."""
        return self.role in ['staff', 'admin']
    
    def __repr__(self):
        return f'<User {self.email}>'


class Resource(db.Model):
    """Resource model representing bookable campus resources."""
    __tablename__ = 'resources'
    
    resource_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True, index=True)  # study-room, equipment, lab, event-space, etc.
    location = db.Column(db.String(200), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)
    images = db.Column(db.Text, nullable=True)  # JSON array of image paths
    availability_rules = db.Column(db.Text, nullable=True)  # JSON blob for recurring availability
    status = db.Column(db.String(20), nullable=False, default='draft')  # draft, published, archived
    requires_approval = db.Column(db.Boolean, default=False)
    equipment_list = db.Column(db.Text, nullable=True)  # JSON array of equipment
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='resource', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='resource', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_images(self):
        """Parse and return list of image paths."""
        import json
        if not self.images:
            return []
        try:
            # Try parsing as JSON array
            return json.loads(self.images)
        except (json.JSONDecodeError, TypeError):
            # Fallback: treat as comma-separated string
            return [img.strip() for img in self.images.split(',') if img.strip()]
    
    def get_average_rating(self):
        """Calculate average rating from reviews."""
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(r.rating for r in reviews) / len(reviews)
    
    def get_total_bookings(self):
        """Get total number of completed bookings."""
        return self.bookings.filter_by(status='completed').count()
    
    def __repr__(self):
        return f'<Resource {self.title}>'


class Booking(db.Model):
    """Booking model representing resource reservations."""
    __tablename__ = 'bookings'
    
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.resource_id'), nullable=False, index=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    start_datetime = db.Column(db.DateTime, nullable=False, index=True)
    end_datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected, cancelled, completed
    purpose = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    google_calendar_event_id = db.Column(db.String(255), nullable=True)  # For calendar sync
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking {self.booking_id} - {self.status}>'


class Message(db.Model):
    """Message model for communication between users."""
    __tablename__ = 'messages'
    
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thread_id = db.Column(db.Integer, nullable=True, index=True)  # For grouping related messages
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    related_booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Message {self.message_id}>'


class Review(db.Model):
    """Review model for resource ratings and feedback."""
    __tablename__ = 'reviews'
    
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.resource_id'), nullable=False, index=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=True)
    is_hidden = db.Column(db.Boolean, default=False)  # For admin moderation
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.review_id} - Rating: {self.rating}>'


class AdminLog(db.Model):
    """Admin log model for tracking administrative actions."""
    __tablename__ = 'admin_logs'
    
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    action = db.Column(db.String(100), nullable=False)  # user_suspend, review_hide, booking_modify, etc.
    target_table = db.Column(db.String(50), nullable=True)
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)  # JSON with action details
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<AdminLog {self.log_id} - {self.action}>'
