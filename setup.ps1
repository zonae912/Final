# Campus Resource Hub - Installation and Setup Script
# Run this script to install dependencies and initialize the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Campus Resource Hub - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10 or higher." -ForegroundColor Red
    exit 1
}

# Check if pip is available
Write-Host "Checking pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ pip not found. Please install pip." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies." -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "Checking .env configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Gray
    
    $envContent = @"
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production

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
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=noreply@campushub.edu
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✓ .env file created!" -ForegroundColor Green
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Initialize database
Write-Host ""
Write-Host "Initializing database..." -ForegroundColor Yellow
python scripts\init_database.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database initialized successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to initialize database." -ForegroundColor Red
    exit 1
}

# Success message
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run the application: python run.py" -ForegroundColor White
Write-Host "2. Open browser: http://localhost:5000" -ForegroundColor White
Write-Host "3. Login with demo account:" -ForegroundColor White
Write-Host "   - Email: admin@campus.edu" -ForegroundColor White
Write-Host "   - Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "To run tests: pytest tests\ -v" -ForegroundColor White
Write-Host ""
