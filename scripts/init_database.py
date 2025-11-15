"""
Database initialization script with sample data
Run this to set up the database and populate it with demo data
"""
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import create_app, db
from src.models.models import User, Resource, Booking, Message, Review, AdminLog
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database and create all tables"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables (caution: this deletes all data!)
        print("Dropping existing tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating tables...")
        db.create_all()
        
        print("✓ Database tables created successfully")
        return app

def create_sample_users(app):
    """Create sample users"""
    with app.app_context():
        print("\nCreating sample users...")
        
        users = [
            # Admin
            User(
                name='Admin User',
                email='admin@campus.edu',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                department='Administration'
            ),
            # Professor Ezona - Admin
            User(
                name='Professor Ezona',
                email='ezona@iu.edu',
                password_hash=generate_password_hash('password'),
                role='admin',
                department='Information Systems'
            ),
            # Staff members
            User(
                name='Dr. Smith',
                email='smith@campus.edu',
                password_hash=generate_password_hash('password123'),
                role='staff',
                department='Science'
            ),
            User(
                name='Prof. Johnson',
                email='johnson@campus.edu',
                password_hash=generate_password_hash('password123'),
                role='staff',
                department='Engineering'
            ),
            User(
                name='Campus Librarian',
                email='library@campus.edu',
                password_hash=generate_password_hash('password123'),
                role='staff',
                department='Library Services'
            ),
            # Students
            User(
                name='John Doe',
                email='john.doe@student.campus.edu',
                password_hash=generate_password_hash('password123'),
                role='student',
                department='Computer Science'
            ),
            User(
                name='Jane Smith',
                email='jane.smith@student.campus.edu',
                password_hash=generate_password_hash('password123'),
                role='student',
                department='Biology'
            ),
            User(
                name='Mike Wilson',
                email='mike.w@student.campus.edu',
                password_hash=generate_password_hash('password123'),
                role='student',
                department='Mathematics'
            ),
            User(
                name='Sarah Jones',
                email='sarah.j@student.campus.edu',
                password_hash=generate_password_hash('password123'),
                role='student',
                department='Chemistry'
            ),
        ]
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        print(f"✓ Created {len(users)} users")
        return users

def create_sample_resources(app, users):
    """Create sample resources"""
    with app.app_context():
        print("\nCreating sample resources...")
        
        # Get staff users
        dr_smith = User.query.filter_by(email='smith@campus.edu').first()
        prof_johnson = User.query.filter_by(email='johnson@campus.edu').first()
        librarian = User.query.filter_by(email='library@campus.edu').first()
        
        resources = [
            # Study Rooms
            Resource(
                title='Quiet Study Room 4A',
                description='Small quiet study room perfect for individual study or small groups. Features whiteboard, natural lighting, and comfortable seating.',
                category='study_room',
                location='Main Library, Level 4',
                capacity=6,
                images='["placeholder_study_room.jpg"]',
                equipment_list='["Whiteboard", "Markers", "Comfortable Chairs", "Power Outlets"]',
                status='published',
                requires_approval=False,
                owner=librarian
            ),
            Resource(
                title='Group Study Room 5B',
                description='Large study room ideal for group projects and collaborative work. Equipped with large table and presentation screen.',
                category='study_room',
                location='Main Library, Level 5',
                capacity=12,
                images='["placeholder_group_room.jpg"]',
                equipment_list='["Large Table", "TV Screen", "HDMI Cable", "Whiteboard", "Power Outlets"]',
                status='published',
                requires_approval=False,
                owner=librarian
            ),
            # Labs
            Resource(
                title='Science Lab A',
                description='Fully equipped science laboratory with safety features and modern equipment. Perfect for chemistry and biology experiments.',
                category='lab',
                location='Science Building, Room 201',
                capacity=20,
                images='["placeholder_lab.jpg"]',
                equipment_list='["Microscopes", "Bunsen Burners", "Lab Benches", "Safety Equipment", "Chemical Storage", "Fume Hoods"]',
                status='published',
                requires_approval=True,
                owner=dr_smith
            ),
            Resource(
                title='Computer Lab B',
                description='State-of-the-art computer lab with 30 high-performance workstations. Ideal for programming courses and data analysis.',
                category='lab',
                location='Engineering Building, Room 105',
                capacity=30,
                images='["placeholder_computer_lab.jpg"]',
                equipment_list='["30 Computers", "Dual Monitors", "Programming Software", "High-speed Internet", "Projector"]',
                status='published',
                requires_approval=False,
                owner=prof_johnson
            ),
            # Equipment
            Resource(
                title='Professional Camera Kit',
                description='Canon EOS R5 with multiple lenses, tripod, and lighting equipment. Perfect for media projects and photography assignments.',
                category='equipment',
                location='Media Center, Equipment Checkout',
                capacity=1,
                images='["placeholder_camera.jpg"]',
                equipment_list='["Canon EOS R5", "24-70mm Lens", "70-200mm Lens", "Tripod", "LED Light", "Camera Bag", "Extra Batteries"]',
                status='published',
                requires_approval=True,
                owner=librarian
            ),
            Resource(
                title='Projector and Screen',
                description='Portable projector (4K, 3000 lumens) with screen. Great for presentations and movie screenings.',
                category='equipment',
                location='IT Department, Room 120',
                capacity=1,
                images='["placeholder_projector.jpg"]',
                equipment_list='["4K Projector", "Portable Screen", "HDMI Cable", "VGA Cable", "Remote Control", "Carrying Case"]',
                status='published',
                requires_approval=False,
                owner=prof_johnson
            ),
            # Event Spaces
            Resource(
                title='Conference Room Delta',
                description='Professional conference room with video conferencing capabilities. Ideal for meetings, seminars, and presentations.',
                category='event_space',
                location='Administration Building, Level 3',
                capacity=25,
                images='["placeholder_conference.jpg"]',
                equipment_list='["Conference Table", "Video Conferencing System", "75-inch Display", "Microphones", "Speakers", "Whiteboard"]',
                status='published',
                requires_approval=True,
                owner=User.query.filter_by(email='admin@campus.edu').first()
            ),
            Resource(
                title='Auditorium',
                description='Large auditorium perfect for lectures, presentations, and events. Professional sound and lighting systems.',
                category='event_space',
                location='Student Center, Main Floor',
                capacity=200,
                images='["placeholder_auditorium.jpg"]',
                equipment_list='["Stage", "Sound System", "Lighting", "Projector", "Screen", "Microphones", "Seating for 200"]',
                status='published',
                requires_approval=True,
                owner=User.query.filter_by(email='admin@campus.edu').first()
            ),
            
            # Godfrey Graduate & Executive Education Center Classrooms
            Resource(
                title='CG 0001 Classroom',
                description='Classroom in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 0001',
                capacity=40,
                images='["images/classrooms/CG 0001.jpg"]',
                equipment_list='["Projector", "Whiteboard", "Tables", "Chairs", "Audio System"]',
                status='published',
                requires_approval=True,
                owner=dr_smith
            ),
            Resource(
                title='CG 0030 Teaching Lab',
                description='Teaching lab in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='lab',
                location='Godfrey Grad & Exec Ed Ctr (CG) 0030',
                capacity=45,
                images='["images/classrooms/CG 0030.jpg"]',
                equipment_list='["Lab Workstations", "Computers", "Projector", "Whiteboard", "Safety Equipment"]',
                status='published',
                requires_approval=True,
                owner=dr_smith
            ),
            Resource(
                title='CG 1008 Classroom',
                description='Classroom in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 1008',
                capacity=25,
                images='["images/classrooms/CG 1008.jpg"]',
                equipment_list='["Projector", "Whiteboard", "Tables", "Chairs", "Audio System"]',
                status='published',
                requires_approval=True,
                owner=dr_smith
            ),
            Resource(
                title='CG 1014 Lecture Hall',
                description='Lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 1014',
                capacity=60,
                images='["images/classrooms/CG 1014.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System", "Tiered Seating"]',
                status='published',
                requires_approval=True,
                owner=prof_johnson
            ),
            Resource(
                title='CG 1022 Lecture Hall',
                description='Lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 1022',
                capacity=60,
                images='["images/classrooms/CG 1022.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System", "Tiered Seating"]',
                status='published',
                requires_approval=True,
                owner=prof_johnson
            ),
            Resource(
                title='CG 1026 Lecture Hall',
                description='Lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 1026',
                capacity=60,
                images='["images/classrooms/CG 1026.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System", "Tiered Seating"]',
                status='published',
                requires_approval=True,
                owner=prof_johnson
            ),
            Resource(
                title='CG 1032 Lecture Hall',
                description='Lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 1032',
                capacity=60,
                images='["images/classrooms/CG 1032.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System", "Tiered Seating"]',
                status='published',
                requires_approval=True,
                owner=prof_johnson
            ),
            Resource(
                title='CG 1034 Lecture Hall',
                description='Large lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 1034',
                capacity=80,
                images='["images/classrooms/CG 1034.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System", "Tiered Seating"]',
                status='published',
                requires_approval=True,
                owner=prof_johnson
            ),
            Resource(
                title='CG 1040 Lecture Hall',
                description='Large lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 1040',
                capacity=80,
                images='["images/classrooms/CG 1040.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System", "Tiered Seating"]',
                status='published',
                requires_approval=True,
                owner=prof_johnson
            ),
            Resource(
                title='CG 1050 Lecture Hall',
                description='Large lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 1050',
                capacity=80,
                images='["images/classrooms/CG 1050.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System", "Tiered Seating"]',
                status='published',
                requires_approval=True,
                owner=prof_johnson
            ),
            Resource(
                title='CG 1056 Lecture Hall',
                description='Large lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 1056',
                capacity=80,
                images='["images/classrooms/Cg 1056.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System", "Tiered Seating"]',
                status='published',
                requires_approval=True,
                owner=prof_johnson
            ),
            Resource(
                title='CG 2061 Lecture Hall',
                description='Lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 2061',
                capacity=60,
                images='["images/classrooms/CG 2061.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System", "Tiered Seating"]',
                status='published',
                requires_approval=True,
                owner=dr_smith
            ),
            Resource(
                title='CG 2063 Lecture Hall',
                description='Lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 2063',
                capacity=40,
                images='["images/classrooms/Cg 2063.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System"]',
                status='published',
                requires_approval=True,
                owner=dr_smith
            ),
            Resource(
                title='CG 2069 Lecture Hall',
                description='Lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 2069',
                capacity=40,
                images='["images/classrooms/CG 2069.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System"]',
                status='published',
                requires_approval=True,
                owner=dr_smith
            ),
            Resource(
                title='CG 2077 Lecture Hall',
                description='Lecture hall in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 2077',
                capacity=40,
                images='["images/classrooms/CG 2077.jpg"]',
                equipment_list='["Projector", "Screen", "Podium", "Microphone", "Audio System"]',
                status='published',
                requires_approval=True,
                owner=dr_smith
            ),
            Resource(
                title='CG 3044 Classroom',
                description='Classroom in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 3044',
                capacity=35,
                images='["images/classrooms/CG 3044.jpg"]',
                equipment_list='["Projector", "Whiteboard", "Tables", "Chairs", "Audio System"]',
                status='published',
                requires_approval=True,
                owner=dr_smith
            ),
            Resource(
                title='CG 3055 Classroom',
                description='Classroom in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='classroom',
                location='Godfrey Grad & Exec Ed Ctr (CG) 3055',
                capacity=48,
                images='["images/classrooms/CG 3055.jpg"]',
                equipment_list='["Projector", "Whiteboard", "Tables", "Chairs", "Audio System"]',
                status='published',
                requires_approval=True,
                owner=prof_johnson
            ),
            Resource(
                title='CG 3075 Teaching Lab',
                description='Teaching lab in Godfrey Graduate & Executive Education Center. Departmentally owned by Business.',
                category='lab',
                location='Godfrey Grad & Exec Ed Ctr (CG) 3075',
                capacity=40,
                images='["images/classrooms/CG 3075.jpg"]',
                equipment_list='["Lab Workstations", "Computers", "Projector", "Whiteboard", "Software Licenses"]',
                status='published',
                requires_approval=True,
                owner=prof_johnson
            ),
        ]
        
        for resource in resources:
            db.session.add(resource)
        
        db.session.commit()
        print(f"✓ Created {len(resources)} resources")
        return resources

def create_sample_bookings(app, users, resources):
    """Create sample bookings"""
    with app.app_context():
        print("\nCreating sample bookings...")
        
        john = User.query.filter_by(email='john.doe@student.campus.edu').first()
        jane = User.query.filter_by(email='jane.smith@student.campus.edu').first()
        mike = User.query.filter_by(email='mike.w@student.campus.edu').first()
        sarah = User.query.filter_by(email='sarah.j@student.campus.edu').first()
        
        study_room = Resource.query.filter_by(title='Quiet Study Room 4A').first()
        lab = Resource.query.filter_by(title='Science Lab A').first()
        camera = Resource.query.filter_by(title='Professional Camera Kit').first()
        
        now = datetime.now()
        
        bookings = [
            # Past booking (completed)
            Booking(
                resource=study_room,
                requester=john,
                start_datetime=now - timedelta(days=7, hours=2),
                end_datetime=now - timedelta(days=7),
                status='approved',
                purpose='Study for final exams',
                notes='Need quiet environment'
            ),
            # Upcoming bookings
            Booking(
                resource=study_room,
                requester=jane,
                start_datetime=now + timedelta(days=1, hours=10),
                end_datetime=now + timedelta(days=1, hours=12),
                status='approved',
                purpose='Group project meeting',
                notes='Working on biology presentation'
            ),
            Booking(
                resource=lab,
                requester=sarah,
                start_datetime=now + timedelta(days=2, hours=14),
                end_datetime=now + timedelta(days=2, hours=16),
                status='approved',
                purpose='Chemistry experiment',
                notes='Testing pH levels'
            ),
            # Pending booking
            Booking(
                resource=camera,
                requester=mike,
                start_datetime=now + timedelta(days=3, hours=9),
                end_datetime=now + timedelta(days=3, hours=17),
                status='pending',
                purpose='Documentary filming',
                notes='Need for media project'
            ),
        ]
        
        for booking in bookings:
            db.session.add(booking)
        
        db.session.commit()
        print(f"✓ Created {len(bookings)} bookings")
        return bookings

def create_sample_reviews(app, bookings):
    """Create sample reviews"""
    with app.app_context():
        print("\nCreating sample reviews...")
        
        # Get past booking
        past_booking = Booking.query.filter(
            Booking.end_datetime < datetime.now()
        ).first()
        
        if past_booking:
            review = Review(
                resource_id=past_booking.resource_id,
                reviewer_id=past_booking.requester_id,
                booking_id=past_booking.booking_id,
                rating=5,
                comment='Excellent study room! Very quiet and comfortable. The whiteboard was very useful for brainstorming. Highly recommend for focused study sessions.'
            )
            
            db.session.add(review)
            db.session.commit()
            print("✓ Created 1 review")
            return [review]
        else:
            print("⚠ No past bookings available for review")
            return []

def create_sample_messages(app, users, bookings):
    """Create sample messages"""
    with app.app_context():
        print("\nCreating sample messages...")
        
        john = User.query.filter_by(email='john.doe@student.campus.edu').first()
        jane = User.query.filter_by(email='jane.smith@student.campus.edu').first()
        dr_smith = User.query.filter_by(email='smith@campus.edu').first()
        sarah = User.query.filter_by(email='sarah.j@student.campus.edu').first()
        
        pending_booking = Booking.query.filter_by(status='pending').first()
        
        messages = [
            # General message
            Message(
                sender_id=john.user_id,
                receiver_id=jane.user_id,
                content='Hey Jane, would you like to join our study group for the biology final? We\'re meeting next week.',
                is_read=False
            ),
            # Booking-related message
            Message(
                sender_id=sarah.user_id,
                receiver_id=dr_smith.user_id,
                content='Hi Dr. Smith, I have a booking for the Science Lab tomorrow. Will the microscopes be available? I need them for my experiment.',
                related_booking_id=Booking.query.filter_by(status='approved').filter(
                    Booking.resource_id == Resource.query.filter_by(title='Science Lab A').first().resource_id
                ).first().booking_id if Booking.query.filter_by(status='approved').filter(
                    Booking.resource_id == Resource.query.filter_by(title='Science Lab A').first().resource_id
                ).first() else None,
                is_read=True
            ),
        ]
        
        for message in messages:
            db.session.add(message)
        
        db.session.commit()
        print(f"✓ Created {len(messages)} messages")
        return messages

def create_sample_admin_logs(app):
    """Create sample admin logs"""
    with app.app_context():
        print("\nCreating sample admin logs...")
        
        admin = User.query.filter_by(role='admin').first()
        
        logs = [
            AdminLog(
                admin_id=admin.user_id,
                action='create',
                target_table='resource',
                target_id=1,
                details='Created Conference Room Delta'
            ),
            AdminLog(
                admin_id=admin.user_id,
                action='approve',
                target_table='booking',
                target_id=1,
                details='Approved booking for study room'
            ),
        ]
        
        for log in logs:
            db.session.add(log)
        
        db.session.commit()
        print(f"✓ Created {len(logs)} admin logs")
        return logs

def main():
    """Main initialization function"""
    print("="*60)
    print("Campus Resource Hub - Database Initialization")
    print("="*60)
    
    # Initialize database
    app = init_database()
    
    # Create sample data
    users = create_sample_users(app)
    resources = create_sample_resources(app, users)
    bookings = create_sample_bookings(app, users, resources)
    reviews = create_sample_reviews(app, bookings)
    messages = create_sample_messages(app, users, bookings)
    logs = create_sample_admin_logs(app)
    
    print("\n" + "="*60)
    print("✓ Database initialization complete!")
    print("="*60)
    print("\nSample credentials:")
    print("-" * 60)
    print("Admin:")
    print("  Email: admin@campus.edu")
    print("  Password: admin123")
    print("\nStaff:")
    print("  Email: smith@campus.edu")
    print("  Password: password123")
    print("\nStudent:")
    print("  Email: john.doe@student.campus.edu")
    print("  Password: password123")
    print("-" * 60)
    print("\nYou can now run the application with: python run.py")
    print("="*60)

if __name__ == '__main__':
    main()


