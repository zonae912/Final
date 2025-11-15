"""
Chatbot controller using Google Gemini AI
Handles FAQ responses and user guidance
"""
from flask import Blueprint, render_template, request, jsonify, current_app, session
from flask_login import login_required, current_user
import google.generativeai as genai
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

def get_gemini_model():
    """Initialize and return Gemini model"""
    genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
    model = genai.GenerativeModel('gemini-pro')
    return model

def get_system_context():
    """Return context about the Campus Resource Hub system for the chatbot"""
    return """You are a helpful AI assistant for the Campus Resource Hub system. 

SYSTEM OVERVIEW:
The Campus Resource Hub is a university resource booking and management platform.

MAIN FEATURES:
1. **Resource Browsing & Search**
   - Students and staff can browse resources by category (study rooms, classrooms, labs, equipment, event spaces)
   - Search by keyword, location, capacity, and availability
   - Filter and sort options available
   - View resource details, ratings, and availability

2. **Booking System**
   - Users can book resources with start/end times
   - Study rooms: Automatic approval (instant confirmation)
   - Classrooms, labs, equipment: Require owner approval (pending status)
   - Recurring bookings supported (daily/weekly/biweekly patterns)
   - Conflict detection prevents double-booking
   - Export bookings to calendar (.ical format)

3. **Reviews & Ratings**
   - After completed bookings, users can rate resources (1-5 stars)
   - Leave feedback for resource owners
   - Top-rated badges for excellent resources (4.0+ average)

4. **Messaging**
   - Internal messaging between users
   - Notifications for booking approvals/rejections
   - Communication with resource owners

5. **User Roles**
   - Students: Can browse, book, and review resources
   - Staff: Can manage their own resources, approve bookings
   - Admin: Full system access, user management, analytics

RESOURCE CATEGORIES:
- **Study Rooms**: Quiet spaces for individual or group study (auto-approved)
- **Classrooms**: Teaching spaces (requires approval)
- **Labs**: Science, computer, and specialized labs (requires approval)
- **Equipment**: Cameras, projectors, scientific instruments (requires approval)
- **Event Spaces**: Conference rooms, auditoriums (requires approval)

COMMON LOCATIONS:
- Main Library (Levels 4-5): Study rooms
- Godfrey Graduate & Executive Education Center (CG): Business classrooms and labs
- Science Building: Science labs
- Engineering Building: Computer labs
- Student Center: Event spaces

FREQUENTLY ASKED QUESTIONS:

**Booking Questions:**
Q: How do I book a resource?
A: Navigate to Resources → Browse or Search, select a resource, click "Book Now", choose date/time, and submit. Study rooms are approved instantly, other resources need owner approval.

Q: Can I book recurring sessions?
A: Yes! When booking, enable the "Recurring Booking" option and choose daily, weekly, or biweekly patterns (up to 10 occurrences).

Q: What if my booking conflicts with another?
A: The system will detect conflicts and notify you. For recurring bookings, conflicting slots are automatically skipped.

Q: How do I cancel a booking?
A: Go to My Bookings, find your booking, and click "Cancel". Please cancel early to allow others to use the resource.

**Resource Questions:**
Q: What resources are available?
A: Study rooms, classrooms, labs (science & computer), equipment (cameras, projectors), and event spaces. Browse the catalog or use search filters.

Q: Do all bookings require approval?
A: No. Study rooms are auto-approved for immediate use. Classrooms, labs, equipment, and event spaces require owner approval.

Q: How can I find available resources?
A: Use the search filters to specify date/time availability, location, capacity, and category. Only available resources will be shown.

**Account Questions:**
Q: How do I create an account?
A: Click "Register" in the navigation menu, fill out the form with your campus email, and submit. Login credentials will be provided.

Q: I forgot my password. What should I do?
A: Click "Login" then "Forgot Password?". Enter your email to receive reset instructions.

Q: Can I update my profile?
A: Yes! Go to your profile page (click your name in navigation) to update your information and change your password.

**Review Questions:**
Q: When can I review a resource?
A: After your booking is completed, you'll see a "Rate your experience!" prompt on the My Bookings page.

Q: What makes a resource "Top Rated"?
A: Resources with 4.5+ average rating and at least 5 reviews receive a "Top Rated" badge. 4.0+ with 3+ reviews get "Excellent" badges.

**Technical Questions:**
Q: Can I export bookings to my calendar?
A: Yes! Each booking has an "Export to Calendar" option that generates an .ical file for Google Calendar, Outlook, or Apple Calendar.

Q: What browsers are supported?
A: Modern browsers: Chrome, Firefox, Safari, Edge (latest versions recommended).

Q: Is there a mobile app?
A: The website is mobile-responsive and works well on phones and tablets. No separate app is needed.

INSTRUCTIONS:
- Be friendly, helpful, and concise
- Provide specific step-by-step guidance when needed
- Direct users to the appropriate pages/features
- If you don't know something specific about the system, admit it and suggest contacting staff
- Use the information above to answer questions accurately
- For booking issues or technical problems, suggest contacting support at support@campus.edu

Always maintain a helpful and professional tone."""

@chatbot_bp.route('/')
@login_required
def index():
    """Chatbot interface page"""
    return render_template('chatbot.html')

@chatbot_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    """Handle chat messages and return AI responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get conversation history from session
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        # Initialize Gemini model
        model = get_gemini_model()
        
        # Build conversation with system context
        chat_session = model.start_chat(history=[])
        
        # Create prompt with system context and user message
        full_prompt = f"""{get_system_context()}

Current user: {current_user.name} ({current_user.role})
User question: {user_message}

Provide a helpful response based on the system information above."""
        
        # Generate response
        response = chat_session.send_message(full_prompt)
        bot_response = response.text
        
        # Store in session history (keep last 20 messages)
        session['chat_history'].append({
            'user': user_message,
            'bot': bot_response,
            'timestamp': datetime.now().isoformat()
        })
        
        if len(session['chat_history']) > 20:
            session['chat_history'] = session['chat_history'][-20:]
        
        session.modified = True
        
        return jsonify({
            'response': bot_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        current_app.logger.error(f"Chatbot error: {str(e)}")
        return jsonify({
            'error': 'Sorry, I encountered an error. Please try again or contact support.',
            'details': str(e)
        }), 500

@chatbot_bp.route('/history', methods=['GET'])
@login_required
def get_history():
    """Get chat history for current user"""
    history = session.get('chat_history', [])
    return jsonify({'history': history})

@chatbot_bp.route('/clear', methods=['POST'])
@login_required
def clear_history():
    """Clear chat history"""
    session['chat_history'] = []
    session.modified = True
    return jsonify({'message': 'Chat history cleared'})
