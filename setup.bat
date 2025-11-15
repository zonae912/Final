@echo off
REM Campus Resource Hub - Quick Setup Script
REM This script installs dependencies and initializes the database

echo ========================================
echo Campus Resource Hub - Setup Script
echo ========================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.10 or higher.
    pause
    exit /b 1
)
echo Python found!
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    (
        echo # Flask Configuration
        echo FLASK_APP=run.py
        echo FLASK_ENV=development
        echo SECRET_KEY=dev-secret-key-change-in-production
        echo.
        echo # Database Configuration
        echo DATABASE_URL=sqlite:///campus_hub.db
        echo.
        echo # Google API Configuration ^(Optional^)
        echo GOOGLE_CLIENT_ID=
        echo GOOGLE_CLIENT_SECRET=
        echo GOOGLE_CSE_API_KEY=
        echo GOOGLE_CSE_ID=
    ) > .env
    echo .env file created!
) else (
    echo .env file already exists.
)
echo.

REM Initialize database
echo Initializing database...
python scripts\init_database.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to initialize database.
    pause
    exit /b 1
)
echo Database initialized successfully!
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run: python run.py
echo 2. Open: http://localhost:5000
echo 3. Login: admin@campus.edu / admin123
echo.
echo To run tests: pytest tests\ -v
echo.
pause
