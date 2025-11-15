# Quick Start Guide - Campus Resource Hub

## 🚀 Get Started in 5 Minutes

### Option 1: Automated Setup (Recommended)

**Run the setup script:**
```powershell
.\setup.bat
```

This will:
- ✓ Install all dependencies
- ✓ Create .env configuration file
- ✓ Initialize database with sample data
- ✓ Prepare the application for first run

### Option 2: Manual Setup

**Step 1: Install Dependencies**
```powershell
pip install -r requirements.txt
```

**Step 2: Create Configuration File**
```powershell
# Copy .env.example to .env (or create manually)
Copy-Item .env.example .env -ErrorAction SilentlyContinue
```

**Step 3: Initialize Database**
```powershell
python scripts\init_database.py
```

## 🎯 Running the Application

```powershell
python run.py
```

Then open your browser to: **http://localhost:5000**

## 🔐 Demo Accounts

After initialization, you can login with these accounts:

### Admin Account
- **Email:** admin@campus.edu
- **Password:** admin123
- **Access:** Full administrative privileges

### Staff Accounts
- **Email:** staff1@campus.edu, staff2@campus.edu, staff3@campus.edu
- **Password:** password123
- **Access:** Can create and manage resources

### Student Accounts
- **Email:** student1@campus.edu, student2@campus.edu, student3@campus.edu, student4@campus.edu
- **Password:** password123
- **Access:** Can browse resources, book, message, and review

## 🧪 Running Tests

```powershell
# All tests
pytest tests\ -v

# With coverage report
pytest tests\ -v --cov=src --cov-report=html

# View coverage report
start htmlcov\index.html
```

## 📁 Project Structure

```
Final/
├── src/                    # Application source code
│   ├── controllers/        # Route handlers (blueprints)
│   ├── data_access/        # Data Access Layer (DAL)
│   ├── models/             # SQLAlchemy models
│   ├── views/              # Jinja2 templates
│   ├── static/             # CSS, JS, images
│   └── utils/              # Helper functions
├── tests/                  # Test suites
├── scripts/                # Utility scripts
├── docs/                   # Documentation
├── config.py               # Configuration classes
├── run.py                  # Application entry point
└── requirements.txt        # Python dependencies
```

## 🎨 Key Features to Try

1. **User Registration & Login**
   - Create a new account or use demo accounts
   - Update profile and change password

2. **Browse Resources**
   - Search and filter resources
   - View detailed resource information
   - Check availability calendar

3. **Book Resources**
   - Create booking requests
   - View your bookings dashboard
   - Export bookings to Google Calendar or iCal

4. **Messaging**
   - Send messages to resource owners
   - Reply to booking-related inquiries
   - Track conversation threads

5. **Reviews & Ratings**
   - Leave reviews after completed bookings
   - Rate resources (1-5 stars)
   - Read community feedback

6. **Admin Panel** (Admin account only)
   - Manage users and resources
   - Approve/reject bookings
   - View analytics dashboard
   - Monitor system activity

## ⚙️ Configuration

Edit `.env` file to configure:

```env
# Development mode
FLASK_ENV=development

# Security (change in production!)
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///campus_hub.db

# Optional: Google Calendar Integration
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# Optional: Google Custom Search
GOOGLE_CSE_API_KEY=your-api-key
GOOGLE_CSE_ID=your-search-engine-id
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Install dependencies
```powershell
pip install -r requirements.txt
```

### Issue: "Database not found"
**Solution:** Initialize database
```powershell
python scripts\init_database.py
```

### Issue: "Tests failing with import errors"
**Solution:** Ensure you're in project root
```powershell
cd "c:\Users\Family\Downloads\MSIS Core\AiDD\Final"
pytest tests\ -v
```

For more troubleshooting help, see `TROUBLESHOOTING.md`

## 📚 Documentation

- **README.md** - Comprehensive overview
- **INSTALL.md** - Detailed installation guide
- **TROUBLESHOOTING.md** - Common issues and solutions
- **API.md** - API endpoint documentation
- **PRD.md** - Product requirements
- **docs/wireframes/** - UI wireframes
- **docs/context/** - Project management artifacts

## 🎓 Development Workflow

```powershell
# 1. Make code changes
code src\controllers\resource_controller.py

# 2. Run tests
pytest tests\ -v

# 3. Test manually
python run.py
# Visit http://localhost:5000

# 4. Check code quality
pytest tests\ -v --cov=src
```

## 🚢 Production Deployment

Before deploying to production:

1. **Update configuration:**
   ```env
   FLASK_ENV=production
   SECRET_KEY=generate-strong-random-key
   SESSION_COOKIE_SECURE=True
   ```

2. **Use production database:**
   ```env
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```

3. **Set up HTTPS** (required for OAuth)

4. **Configure email** (for notifications)

5. **Set up Google APIs** (for calendar and search features)

See `README.md` for detailed production deployment instructions.

## 📞 Need Help?

- Check **TROUBLESHOOTING.md** for common issues
- Review **INSTALL.md** for detailed setup steps
- Read **API.md** for endpoint documentation
- See **README.md** for feature documentation

---

**Happy Coding! 🎉**

*Campus Resource Hub v1.0.0*
*AiDD 2025 Capstone Project*
