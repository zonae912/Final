# Troubleshooting Guide - Campus Resource Hub

## Common Issues and Solutions

### 1. Import Errors (ModuleNotFoundError)

**Problem:** `ModuleNotFoundError: No module named 'flask'` or similar import errors.

**Solution:**
```powershell
# Install all required packages
pip install -r requirements.txt

# Or install individually:
pip install Flask==3.0.0 Flask-Login==0.6.3 Flask-WTF==1.2.1 Flask-SQLAlchemy==3.1.1
pip install bcrypt==4.1.1 python-dotenv==1.0.0 pytest==7.4.3 pytest-flask==1.3.0
pip install bleach==6.1.0 python-dateutil==2.8.2 pytz==2023.3 pytest-cov
```

### 2. Test Collection Errors

**Problem:** `ModuleNotFoundError: No module named 'src'`

**Solution:** The `conftest.py` file has been created at the project root to fix Python path issues.

If still having issues:
```powershell
# Run from project root
cd "c:\Users\Family\Downloads\MSIS Core\AiDD\Final"

# Set PYTHONPATH
$env:PYTHONPATH = "c:\Users\Family\Downloads\MSIS Core\AiDD\Final"

# Run tests
pytest tests\ -v
```

### 3. Database Errors

**Problem:** Database doesn't exist or tables not created.

**Solution:**
```powershell
# Initialize database with sample data
python scripts\init_database.py

# Or manually:
python -c "from src import create_app; from src.models.models import db; app = create_app(); app.app_context().push(); db.create_all()"
```

### 4. Flask Application Won't Start

**Problem:** `RuntimeError: Working outside of application context`

**Solution:**
```powershell
# Make sure you're running from project root
python run.py

# Or use Flask CLI
flask run
```

### 5. CSRF Token Errors

**Problem:** CSRF validation errors in forms.

**Solution:** Check that:
- `WTF_CSRF_ENABLED = True` in config.py (except for TestingConfig)
- Forms include `{{ form.csrf_token }}` or use `form.hidden_tag()`
- SECRET_KEY is set in .env file

### 6. File Upload Errors

**Problem:** Images not uploading or 413 error.

**Solution:**
```python
# Check MAX_CONTENT_LENGTH in config.py (currently 16MB)
# Create uploads directory if it doesn't exist
mkdir src\static\uploads
mkdir src\static\uploads\resources
mkdir src\static\uploads\profiles
```

### 7. Google API Errors

**Problem:** Google Calendar/Search not working.

**Solution:**
```powershell
# Install Google API packages
pip install google-api-python-client==2.108.0 google-auth==2.25.2
pip install google-auth-oauthlib==1.2.0 google-auth-httplib2==0.2.0

# Add credentials to .env file
# GOOGLE_CLIENT_ID=your-client-id
# GOOGLE_CLIENT_SECRET=your-client-secret
# GOOGLE_CSE_API_KEY=your-api-key
# GOOGLE_CSE_ID=your-search-engine-id
```

### 8. Session/Login Errors

**Problem:** Users can't stay logged in or session expires immediately.

**Solution:**
```python
# Check in config.py:
SECRET_KEY = 'your-secret-key-here'  # Must be set
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
SESSION_COOKIE_HTTPONLY = True
```

### 9. Template Not Found Errors

**Problem:** `TemplateNotFound: base.html`

**Solution:**
```powershell
# Check template_folder in src/__init__.py
# Should be: template_folder='views'

# Verify templates exist:
dir src\views\*.html -Recurse
```

### 10. Migration/Schema Errors

**Problem:** Database schema out of sync with models.

**Solution:**
```powershell
# Drop and recreate database
python -c "from src import create_app; from src.models.models import db; app = create_app(); app.app_context().push(); db.drop_all(); db.create_all()"

# Or re-run init script
python scripts\init_database.py
```

## Quick Fixes

### Reset Everything
```powershell
# Delete database
Remove-Item campus_hub.db -ErrorAction SilentlyContinue

# Reinstall packages
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Reinitialize database
python scripts\init_database.py

# Run application
python run.py
```

### Clean Test Environment
```powershell
# Clear pytest cache
Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue

# Clear Python cache
Get-ChildItem -Recurse -Directory __pycache__ | Remove-Item -Recurse -Force

# Run tests fresh
pytest tests\ -v --cache-clear
```

### Verify Installation
```powershell
# Check Python version (should be 3.10+)
python --version

# Check installed packages
pip list | Select-String -Pattern "Flask|pytest|bcrypt|bleach"

# Check project structure
tree /F src

# Verify configuration
python -c "from config import config; print(config['development'].SQLALCHEMY_DATABASE_URI)"
```

## Running Tests Successfully

### Basic Test Run
```powershell
# All tests
pytest tests\ -v

# Specific test file
pytest tests\test_auth.py -v

# Specific test function
pytest tests\test_auth.py::test_register -v

# With coverage
pytest tests\ -v --cov=src --cov-report=html
```

### Test Markers
```powershell
# Unit tests only
pytest tests\ -v -m unit

# Integration tests only
pytest tests\ -v -m integration

# Auth tests
pytest tests\ -v -m auth

# DAL tests
pytest tests\ -v -m dal
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///campus_hub.db

# Google API Configuration (Optional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_CSE_API_KEY=
GOOGLE_CSE_ID=

# Email Configuration (Optional)
MAIL_SERVER=localhost
MAIL_PORT=25
MAIL_USE_TLS=false
```

## System Requirements

- **Python**: 3.10 or higher
- **pip**: Latest version (update with `python -m pip install --upgrade pip`)
- **Operating System**: Windows 10/11, macOS, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB free space for dependencies

## Getting Help

If you encounter issues not covered here:

1. Check the error message carefully
2. Review the relevant documentation in `docs/`
3. Check `README.md` for feature-specific help
4. Verify all dependencies are installed: `pip list`
5. Ensure you're in the correct directory (project root)
6. Check file permissions for database and upload directories

## Additional Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **pytest Documentation**: https://docs.pytest.org/
- **Bootstrap Documentation**: https://getbootstrap.com/docs/5.3/

---

**Last Updated:** November 11, 2025
