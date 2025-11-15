# AI Contribution: Copilot structured application entry point
# Reviewed and approved by team

"""
Application entry point for Campus Resource Hub
Run this file to start the Flask development server.
"""

import os
from src import create_app
from src.models.models import db

# Create Flask application
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config.get('DEBUG', True)
    )
