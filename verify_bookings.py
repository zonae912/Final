"""
Verification script to check if bookings are properly linked to users.
"""
from config import Config
from src.models.models import db, User, Booking, Resource
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    print("=" * 60)
    print("BOOKING VERIFICATION REPORT")
    print("=" * 60)
    
    # Get all users
    users = User.query.all()
    print(f"\nTotal users in database: {len(users)}")
    
    # Get all bookings
    bookings = Booking.query.all()
    print(f"Total bookings in database: {len(bookings)}")
    
    if not bookings:
        print("\nNo bookings found in database.")
    else:
        print("\n" + "-" * 60)
        print("BOOKINGS BY USER:")
        print("-" * 60)
        
        for user in users:
            user_bookings = Booking.query.filter_by(requester_id=user.user_id).all()
            if user_bookings:
                print(f"\nUser: {user.name} ({user.email})")
                print(f"  User ID: {user.user_id}")
                print(f"  Number of bookings: {len(user_bookings)}")
                
                for booking in user_bookings:
                    resource = Resource.query.get(booking.resource_id)
                    print(f"    - Booking #{booking.booking_id}: {resource.title if resource else 'Unknown Resource'}")
                    print(f"      Status: {booking.status}")
                    print(f"      Start: {booking.start_datetime}")
                    print(f"      Requester ID: {booking.requester_id}")
        
        # Check for orphaned bookings (bookings with invalid requester_id)
        print("\n" + "-" * 60)
        print("CHECKING FOR ORPHANED BOOKINGS:")
        print("-" * 60)
        orphaned = []
        for booking in bookings:
            user = User.query.get(booking.requester_id)
            if not user:
                orphaned.append(booking)
        
        if orphaned:
            print(f"\n⚠ WARNING: Found {len(orphaned)} orphaned bookings!")
            for booking in orphaned:
                print(f"  - Booking #{booking.booking_id} has invalid requester_id: {booking.requester_id}")
        else:
            print("\n✓ All bookings have valid requester_id")
    
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)
