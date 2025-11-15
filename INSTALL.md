# Campus Resource Hub - Installation & Testing Guide

## 📋 Prerequisites

- **Python 3.10 or higher**
- **pip** (Python package installer)
- **Git** (for version control)
- **Google API Credentials** (for Calendar and Search APIs)

---

## 🚀 Installation Steps

### 1. Navigate to Project Directory
```powershell
cd "c:\Users\Family\Downloads\MSIS Core\AiDD\Final"
```

### 2. Create Virtual Environment
```powershell
python -m venv venv
```

### 3. Activate Virtual Environment
```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# If you encounter execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

**Expected installation time**: 2-5 minutes depending on internet speed.

---

## 🔧 Configuration

### 1. Create Environment File
```powershell
Copy-Item .env.example .env
```

### 2. Edit Configuration
Open `.env` in your text editor and configure:

```env
# Application Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-this

# Database Configuration
DATABASE_URL=sqlite:///campus_hub.db

# Google API Configuration (for advanced features)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_SEARCH_API_KEY=your-google-search-api-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id

# File Upload Configuration
MAX_CONTENT_LENGTH=5242880
UPLOAD_FOLDER=src/static/uploads
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif

# Security Configuration
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

**Note**: For development, you can skip Google API configuration. The app will work without it (calendar sync and advanced search won't be available).

### 3. Generate Secret Key
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output and paste it as your `SECRET_KEY` in `.env`.

---

## 🗄️ Database Setup

### Option 1: Initialize with Sample Data (Recommended for Demo)
```powershell
python scripts/init_database.py
```

This will create:
- 8 sample users (1 admin, 3 staff, 4 students)
- 8 sample resources (study rooms, labs, equipment, event spaces)
- 4 sample bookings (past, upcoming, pending)
- Sample reviews and messages

**Sample Credentials**:
- **Admin**: admin@campus.edu / admin123
- **Staff**: smith@campus.edu / password123
- **Student**: john.doe@student.campus.edu / password123

### Option 2: Initialize Empty Database
```powershell
python -c "from src import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database created')"
```

---

## ▶️ Running the Application

### Start the Development Server
```powershell
python run.py
```

Expected output:
```
 * Serving Flask app 'src'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

or

```
http://127.0.0.1:5000
```

---

## ✅ Testing the Application

### Run All Tests
```powershell
pytest tests/ -v
```

### Run Specific Test Files
```powershell
# Authentication tests
pytest tests/test_auth.py -v

# Data Access Layer tests
pytest tests/test_dal.py -v
```

### Run Tests with Coverage
```powershell
pytest tests/ --cov=src --cov-report=html
```

Then open `htmlcov/index.html` in your browser to view the coverage report.

### Run Tests by Marker
```powershell
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Authentication tests
pytest -m auth
```

---

## 🧪 Manual Testing Checklist

### 1. User Registration & Authentication
- [ ] Register a new account
- [ ] Log in with new account
- [ ] Access protected pages
- [ ] Log out
- [ ] Update profile
- [ ] Change password

### 2. Resource Management
- [ ] Browse resources
- [ ] Search for resources
- [ ] Filter by category/location
- [ ] View resource details
- [ ] Create a new resource (staff only)
- [ ] Edit own resource
- [ ] Delete own resource

### 3. Booking System
- [ ] Create a booking
- [ ] Verify conflict detection (try overlapping times)
- [ ] View my bookings
- [ ] Cancel a booking
- [ ] Export booking to iCal
- [ ] Approve/reject bookings (resource owner)

### 4. Messaging
- [ ] Send a message
- [ ] Reply to a message
- [ ] View message threads
- [ ] Link message to booking

### 5. Reviews
- [ ] Write a review (after completed booking)
- [ ] Edit own review
- [ ] Delete own review
- [ ] View resource ratings

### 6. Admin Functions
- [ ] Access admin dashboard
- [ ] Manage users
- [ ] Manage resources
- [ ] View bookings
- [ ] Moderate reviews
- [ ] View audit logs
- [ ] View analytics

### 7. Google Calendar Integration (if configured)
- [ ] Connect Google Calendar
- [ ] Sync booking to Google Calendar
- [ ] Disconnect Google Calendar

---

## 🐛 Troubleshooting

### Issue: Virtual environment won't activate
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Issue: Package installation fails
**Solution**:
```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**:
```powershell
# Delete existing database
Remove-Item campus_hub.db -ErrorAction SilentlyContinue

# Reinitialize
python scripts/init_database.py
```

### Issue: Port 5000 already in use
**Solution**:
```powershell
# Use a different port
$env:FLASK_RUN_PORT="5001"
python run.py
```

### Issue: Import errors
**Solution**:
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: CSRF token errors
**Solution**:
1. Make sure `SECRET_KEY` is set in `.env`
2. Clear browser cookies
3. Restart the application

### Issue: File upload errors
**Solution**:
```powershell
# Create uploads directory
New-Item -Path "src/static/uploads" -ItemType Directory -Force
```

---

## 📊 Verifying Installation

### Check Python Version
```powershell
python --version
```
Should be 3.10 or higher.

### Check Installed Packages
```powershell
pip list
```
Verify Flask, SQLAlchemy, and other dependencies are installed.

### Check Database
```powershell
python -c "from src import create_app, db; from src.models.models import User; app = create_app(); app.app_context().push(); print(f'Users in database: {User.query.count()}')"
```

### Run Quick Test
```powershell
python -c "from src import create_app; app = create_app(); print('✓ App created successfully')"
```

---

## 🔐 Security Notes

1. **Never commit `.env` file** to version control
2. **Change default passwords** before deployment
3. **Generate strong SECRET_KEY** for production
4. **Use HTTPS** in production
5. **Set `FLASK_ENV=production`** for production
6. **Disable DEBUG mode** in production

---

## 🌐 Production Deployment (Optional)

### Using Gunicorn (WSGI Server)
```powershell
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "src:create_app()"
```

### Environment Variables for Production
```env
FLASK_ENV=production
SECRET_KEY=very-strong-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/campus_hub
SESSION_COOKIE_SECURE=True
```

---

## 📝 Next Steps

1. **Explore the Application**: Log in with sample accounts and test features
2. **Customize Content**: Add your own resources and bookings
3. **Configure Google APIs**: Set up Calendar and Search integration
4. **Run Tests**: Ensure everything works correctly
5. **Deploy**: Follow production deployment guide when ready

---

## 📧 Support

For issues or questions:
- Check `SUBMISSION_CHECKLIST.md` for comprehensive feature documentation
- Review `README.md` for detailed project information
- Consult `docs/API.md` for API endpoint documentation

---

## ✨ Quick Start Summary

```powershell
# 1. Setup
cd "c:\Users\Family\Downloads\MSIS Core\AiDD\Final"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Configure
Copy-Item .env.example .env
# Edit .env with your settings

# 3. Initialize Database
python scripts/init_database.py

# 4. Run Application
python run.py

# 5. Access at http://localhost:5000
# Login with: admin@campus.edu / admin123
```

---

**Installation Complete!** 🎉

You're ready to use Campus Resource Hub. Enjoy exploring all the features!
