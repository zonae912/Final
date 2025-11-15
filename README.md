# Campus Resource Hub
## AI-First Development Project | MSIS Core - AiDD 2025

A comprehensive full-stack web application for managing and reserving campus resources including study rooms, equipment, lab instruments, event spaces, and more.

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [AI-First Development](#ai-first-development)
- [Advanced Features](#advanced-features)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Security Features](#security-features)
- [Team & Contributors](#team--contributors)

---

## 🎯 Project Overview

Campus Resource Hub enables university departments, student organizations, and individuals to list, share, and reserve campus resources efficiently. The system supports search, booking with calendar integration, role-based access control, ratings and reviews, and comprehensive administrative workflows.

**Project Duration**: 18 days  
**Course**: AI Driven Development (AiDD / X501)  
**Instructor**: Prof. Jay Newquist  
**Due Date**: November 15, 2025

---

## ✨ Features

### Core Features
- ✅ **User Management & Authentication**
  - Registration, login, logout with bcrypt password hashing
  - Role-based access control (Student, Staff, Admin)
  - Profile management and password change

- ✅ **Resource Management**
  - Full CRUD operations for resources
  - Image uploads with secure file handling
  - Category-based organization
  - Resource lifecycle management (draft, published, archived)

- ✅ **Search & Filter**
  - Keyword search across title and description
  - Category, location, and capacity filters
  - Sort by recent, most booked, or top-rated
  - **Advanced: Google Custom Search API integration**

- ✅ **Booking & Scheduling**
  - Calendar-based booking interface
  - Real-time conflict detection
  - Approval workflows for restricted resources
  - Email/message notifications
  - **Advanced: Google Calendar OAuth integration**
  - **Advanced: iCal export functionality**

- ✅ **Messaging System**
  - Direct messaging between users
  - Threaded conversations
  - Unread message indicators
  - Booking-related notifications

- ✅ **Reviews & Ratings**
  - 1-5 star rating system
  - Text reviews with validation
  - Aggregate rating calculations
  - Rating distribution visualization

- ✅ **Admin Dashboard**
  - User, resource, and booking management
  - Review moderation
  - Comprehensive audit logging
  - Usage analytics and reports

### Advanced Features
- 🔍 **Google Custom Search API** - Enhanced resource discovery
- 📅 **Google Calendar OAuth** - Two-way calendar synchronization
- 📥 **iCal Export** - Standard calendar format export
- 🤖 **AI Resource Concierge** - Context-aware assistant (MCP integration)

---

## 🛠 Technology Stack

### Backend
- **Python 3.10+** - Core language
- **Flask 3.0** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **Flask-WTF** - CSRF protection and form handling
- **bcrypt** - Password hashing
- **SQLite** - Database (PostgreSQL ready)

### Frontend
- **Jinja2** - Template engine
- **Bootstrap 5.3** - CSS framework
- **Bootstrap Icons** - Icon library
- **Vanilla JavaScript** - Client-side interactions

### APIs & Integration
- **Google Calendar API** - Calendar synchronization
- **Google Custom Search API** - Advanced search
- **iCalendar** - Calendar export standard

### Testing & Quality
- **pytest** - Testing framework
- **pytest-flask** - Flask testing utilities

### Security
- **CSRF Protection** - Flask-WTF tokens
- **XSS Prevention** - Bleach HTML sanitization
- **SQL Injection Protection** - SQLAlchemy ORM
- **Secure Password Storage** - bcrypt hashing

---

## 📁 Project Structure

```
Campus-Resource-Hub/
├── .prompt/                          # AI-First development logs
│   ├── dev_notes.md                  # AI interaction documentation
│   └── golden_prompts.md             # High-impact prompts
├── docs/                             # Documentation
│   └── context/                      # Context Pack for AI tools
│       ├── APA/                      # Agility, Processes & Automation artifacts
│       ├── DT/                       # Design Thinking artifacts
│       ├── PM/                       # Product Management artifacts
│       └── shared/                   # Common artifacts
├── src/                              # Application source code
│   ├── controllers/                  # Flask route handlers
│   │   ├── auth_controller.py
│   │   ├── main_controller.py
│   │   ├── resource_controller.py
│   │   ├── booking_controller.py
│   │   ├── message_controller.py
│   │   ├── review_controller.py
│   │   ├── admin_controller.py
│   │   └── calendar_controller.py
│   ├── models/                       # Database models
│   │   └── models.py
│   ├── data_access/                  # Data Access Layer (DAL)
│   │   ├── user_dal.py
│   │   ├── resource_dal.py
│   │   ├── booking_dal.py
│   │   ├── message_dal.py
│   │   ├── review_dal.py
│   │   └── admin_log_dal.py
│   ├── views/                        # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   ├── resources/
│   │   ├── bookings/
│   │   ├── messages/
│   │   ├── reviews/
│   │   ├── admin/
│   │   └── errors/
│   ├── static/                       # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── uploads/
│   └── __init__.py                   # Application factory
├── tests/                            # Test suite
│   ├── ai_eval/                      # AI feature tests
│   ├── test_auth.py
│   ├── test_resources.py
│   ├── test_bookings.py
│   └── test_dal.py
├── config.py                         # Configuration settings
├── run.py                            # Application entry point
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git
- Google Cloud Project (for Calendar & Search APIs)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Campus-Resource-Hub
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
```bash
# Copy the example environment file
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Edit .env and add your configuration
notepad .env  # Windows
# nano .env  # macOS/Linux
```

**Required Environment Variables:**
```
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-oauth-client-id
GOOGLE_CLIENT_SECRET=your-google-oauth-client-secret
GOOGLE_CSE_API_KEY=your-google-custom-search-api-key
GOOGLE_CSE_ID=your-custom-search-engine-id
```

### Step 5: Initialize Database
```bash
python
>>> from src import create_app
>>> from src.models.models import db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Step 6: Create Admin User (Optional)
```bash
python create_admin.py
```

---

## 🏃 Running the Application

### Development Server
```bash
python run.py
```

Visit `http://localhost:5000` in your web browser.

### Production Deployment
For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "src:create_app()"
```

---

## 🤖 AI-First Development

This project follows AI-First Development principles as required by the AiDD 2025 curriculum.

### AI Tools Used
- **GitHub Copilot Agent Mode** - Code generation and refactoring
- **Cursor AI** - Context-aware development assistance

### AI Contribution Documentation
All AI-assisted development is documented in:
- `.prompt/dev_notes.md` - Comprehensive interaction log
- `.prompt/golden_prompts.md` - Most effective prompts
- Code attribution comments in source files

### Context Pack Structure
The `/docs/context/` directory contains artifacts that help AI tools understand:
- **APA/** - Process models and acceptance tests
- **DT/** - User personas and journey maps
- **PM/** - Product requirements and OKRs
- **shared/** - Common vocabulary and glossary

### AI Integration in Code
Example of AI attribution in code:
```python
# AI Contribution: Copilot generated booking conflict detection logic
# Reviewed and modified by team for edge case handling
```

---

## 🔥 Advanced Features

### 1. Google Custom Search API Integration

**Purpose**: Enhanced resource discovery beyond local database

**Setup**:
1. Create Google Custom Search Engine at https://cse.google.com
2. Configure to search your domain or resource URLs
3. Add API key and Search Engine ID to `.env`

**Usage**: Automatically integrated into main search functionality

### 2. Google Calendar OAuth Integration

**Purpose**: Two-way synchronization with user's Google Calendar

**Setup**:
1. Create OAuth 2.0 credentials in Google Cloud Console
2. Add authorized redirect URIs: `http://localhost:5000/calendar/oauth/callback`
3. Add credentials to `.env`

**Features**:
- Connect/disconnect Google Calendar from user profile
- Sync individual bookings to Google Calendar
- Automatic event creation with reminders

### 3. iCal Export

**Purpose**: Universal calendar format compatible with all calendar apps

**Features**:
- Export individual booking as `.ics` file
- Export all user bookings as single calendar file
- Compatible with Outlook, Apple Calendar, Google Calendar

---

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Test Coverage
- Unit tests for all DAL methods
- Integration tests for auth flow
- Booking conflict detection tests
- Security vulnerability tests

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Resource CRUD operations
- [ ] Booking creation with conflict detection
- [ ] Calendar synchronization
- [ ] iCal export functionality
- [ ] Admin panel operations
- [ ] Review submission
- [ ] Message sending

---

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - Create new user account
- `POST /auth/login` - Authenticate user
- `GET /auth/logout` - Log out current user
- `GET /auth/profile` - View/edit user profile

### Resource Endpoints
- `GET /resources/` - List all published resources
- `GET /resources/<id>` - View resource details
- `POST /resources/create` - Create new resource (auth required)
- `PUT /resources/<id>/edit` - Update resource (owner/admin)
- `DELETE /resources/<id>/delete` - Delete resource (owner/admin)

### Booking Endpoints
- `POST /bookings/create/<resource_id>` - Create booking
- `GET /bookings/<id>` - View booking details
- `POST /bookings/<id>/approve` - Approve booking (owner/staff)
- `POST /bookings/<id>/reject` - Reject booking
- `POST /bookings/<id>/cancel` - Cancel booking
- `GET /bookings/api/check-availability/<resource_id>` - Check availability (JSON)

### Calendar Endpoints
- `GET /calendar/connect` - Initiate Google OAuth
- `GET /calendar/oauth/callback` - OAuth callback handler
- `POST /calendar/sync/<booking_id>` - Sync to Google Calendar
- `GET /calendar/export/<booking_id>.ics` - Export booking as iCal
- `GET /calendar/export-all.ics` - Export all bookings

### Admin Endpoints (Admin Only)
- `GET /admin/dashboard` - Admin overview
- `GET /admin/users` - Manage users
- `GET /admin/resources` - Manage resources
- `GET /admin/bookings` - Manage bookings
- `GET /admin/reviews` - Moderate reviews
- `GET /admin/logs` - View audit logs
- `GET /admin/analytics` - Usage analytics

---

## 🔒 Security Features

### Implemented Security Measures

1. **Authentication & Authorization**
   - Secure password hashing with bcrypt
   - Role-based access control (RBAC)
   - Session management with Flask-Login

2. **Input Validation**
   - Server-side validation for all forms
   - Client-side validation for UX
   - Type checking and length limits

3. **XSS Prevention**
   - Bleach library for HTML sanitization
   - Jinja2 auto-escaping enabled
   - Content Security Policy headers

4. **CSRF Protection**
   - Flask-WTF CSRF tokens
   - Token validation on all state-changing requests

5. **SQL Injection Prevention**
   - SQLAlchemy ORM with parameterized queries
   - No raw SQL in application code

6. **File Upload Security**
   - File type restrictions
   - Secure filename handling (werkzeug)
   - Size limitations (16MB max)
   - Upload directory outside web root

7. **Session Security**
   - HTTP-only cookies
   - Secure flag in production
   - SameSite attribute set

---

## 👥 Team & Contributors

**Team**: Core Team  
**Course**: MSIS Core - AI Driven Development (AiDD/X501)  
**Institution**: Kelley School of Business  
**Semester**: Fall 2025

**Roles**:
- Product Lead / PM
- Backend Engineer
- Frontend Engineer / UX
- Quality & DevOps / Security

---

## 📝 License

This project is developed for educational purposes as part of the MSIS Core curriculum.

---

## 📧 Support

For questions or issues, please contact the course instructor or refer to the project documentation in `/docs/`.

---

## 🎓 Academic Integrity Statement

This project follows AI-First Development principles as outlined in the course syllabus. All AI assistance has been documented transparently in `.prompt/dev_notes.md`. No unreviewed AI-generated content has been submitted as final work.

---

**Last Updated**: November 11, 2025  
**Version**: 1.0.0
