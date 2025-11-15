# AI Contribution: Copilot generated template creation script
# This script creates all necessary HTML templates for the Campus Resource Hub

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIEWS_DIR = os.path.join(BASE_DIR, 'src', 'views')

# Template definitions
TEMPLATES = {
    # Auth templates
    'auth/login.html': '''{% extends "base.html" %}
{% block title %}Login - Campus Resource Hub{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0"><i class="bi bi-box-arrow-in-right"></i> Login</h3>
            </div>
            <div class="card-body">
                <form method="POST" action="{{ url_for('auth.login') }}">
                    {{ csrf_token() }}
                    <div class="mb-3">
                        <label for="email" class="form-label">Email Address *</label>
                        <input type="email" class="form-control" id="email" name="email" required autofocus>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password *</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="remember" name="remember">
                        <label class="form-check-label" for="remember">Remember me</label>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
            </div>
            <div class="card-footer text-center">
                Don't have an account? <a href="{{ url_for('auth.register') }}">Register here</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'auth/register.html': '''{% extends "base.html" %}
{% block title %}Register - Campus Resource Hub{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0"><i class="bi bi-person-plus"></i> Create Account</h3>
            </div>
            <div class="card-body">
                <form method="POST" action="{{ url_for('auth.register') }}">
                    {{ csrf_token() }}
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="name" class="form-label">Full Name *</label>
                            <input type="text" class="form-control" id="name" name="name" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="email" class="form-label">Email Address *</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="password" class="form-label">Password *</label>
                            <input type="password" class="form-control" id="password" name="password" required minlength="8">
                            <small class="form-text text-muted">At least 8 characters</small>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="confirm_password" class="form-label">Confirm Password *</label>
                            <input type="password" class="form-control" id="confirm_password" name="confirm_password" required>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="role" class="form-label">Role *</label>
                            <select class="form-select" id="role" name="role" required>
                                <option value="student">Student</option>
                                <option value="staff">Staff</option>
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="department" class="form-label">Department (Optional)</label>
                            <input type="text" class="form-control" id="department" name="department">
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Register</button>
                </form>
            </div>
            <div class="card-footer text-center">
                Already have an account? <a href="{{ url_for('auth.login') }}">Login here</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'auth/profile.html': '''{% extends "base.html" %}
{% block title %}My Profile{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8 mx-auto">
        <h2><i class="bi bi-person-circle"></i> My Profile</h2>
        <div class="card mt-3">
            <div class="card-body">
                <form method="POST">
                    {{ csrf_token() }}
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="text" class="form-control" value="{{ user.email }}" disabled>
                    </div>
                    <div class="mb-3">
                        <label for="name" class="form-label">Name</label>
                        <input type="text" class="form-control" id="name" name="name" value="{{ user.name }}" required>
                    </div>
                    <div class="mb-3">
                        <label for="department" class="form-label">Department</label>
                        <input type="text" class="form-control" id="department" name="department" value="{{ user.department or '' }}">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Role</label>
                        <input type="text" class="form-control" value="{{ user.role | title }}" disabled>
                    </div>
                    <button type="submit" class="btn btn-primary">Update Profile</button>
                    <a href="{{ url_for('auth.change_password') }}" class="btn btn-outline-secondary">Change Password</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'auth/change_password.html': '''{% extends "base.html" %}
{% block title %}Change Password{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-6 mx-auto">
        <h2>Change Password</h2>
        <div class="card mt-3">
            <div class="card-body">
                <form method="POST">
                    {{ csrf_token() }}
                    <div class="mb-3">
                        <label for="current_password" class="form-label">Current Password</label>
                        <input type="password" class="form-control" id="current_password" name="current_password" required>
                    </div>
                    <div class="mb-3">
                        <label for="new_password" class="form-label">New Password</label>
                        <input type="password" class="form-control" id="new_password" name="new_password" required minlength="8">
                    </div>
                    <div class="mb-3">
                        <label for="confirm_password" class="form-label">Confirm New Password</label>
                        <input type="password" class="form-control" id="confirm_password" name="confirm_password" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Change Password</button>
                    <a href="{{ url_for('auth.profile') }}" class="btn btn-outline-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'dashboard.html': '''{% extends "base.html" %}
{% block title %}Dashboard{% endblock %}
{% block content %}
<h2><i class="bi bi-speedometer2"></i> Dashboard</h2>
<div class="row mt-4">
    <div class="col-md-6">
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="bi bi-calendar-check"></i> Upcoming Bookings</h5>
            </div>
            <div class="list-group list-group-flush">
                {% for booking in upcoming_bookings %}
                <a href="{{ url_for('booking.detail', booking_id=booking.booking_id) }}" class="list-group-item list-group-item-action">
                    <div class="d-flex justify-content-between">
                        <strong>{{ booking.resource.title }}</strong>
                        <span class="badge bg-success">{{ booking.status | title }}</span>
                    </div>
                    <small class="text-muted">{{ booking.start_datetime | datetime_format }}</small>
                </a>
                {% else %}
                <div class="list-group-item">No upcoming bookings</div>
                {% endfor %}
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card mb-4">
            <div class="card-header bg-info text-white">
                <h5 class="mb-0"><i class="bi bi-box"></i> My Resources</h5>
            </div>
            <div class="list-group list-group-flush">
                {% for resource in my_resources[:5] %}
                <a href="{{ url_for('resource.detail', resource_id=resource.resource_id) }}" class="list-group-item list-group-item-action">
                    {{ resource.title }}
                    <span class="badge bg-secondary">{{ resource.status }}</span>
                </a>
                {% else %}
                <div class="list-group-item">No resources yet</div>
                {% endfor %}
            </div>
            <div class="card-footer">
                <a href="{{ url_for('resource.create') }}" class="btn btn-sm btn-primary">Add New Resource</a>
            </div>
        </div>
    </div>
</div>
{% if pending_approvals %}
<div class="alert alert-warning">
    <strong><i class="bi bi-exclamation-triangle"></i> {{ pending_approvals | length }} pending booking approval(s)</strong>
</div>
{% endif %}
{% endblock %}''',

    'errors/404.html': '''{% extends "base.html" %}
{% block title %}Page Not Found{% endblock %}
{% block content %}
<div class="text-center my-5">
    <h1 class="display-1">404</h1>
    <p class="lead">Page not found</p>
    <a href="{{ url_for('main.index') }}" class="btn btn-primary">Go Home</a>
</div>
{% endblock %}''',

    'errors/403.html': '''{% extends "base.html" %}
{% block title %}Access Denied{% endblock %}
{% block content %}
<div class="text-center my-5">
    <h1 class="display-1">403</h1>
    <p class="lead">Access Denied</p>
    <a href="{{ url_for('main.index') }}" class="btn btn-primary">Go Home</a>
</div>
{% endblock %}''',

    'errors/500.html': '''{% extends "base.html" %}
{% block title %}Server Error{% endblock %}
{% block content %}
<div class="text-center my-5">
    <h1 class="display-1">500</h1>
    <p class="lead">Internal Server Error</p>
    <a href="{{ url_for('main.index') }}" class="btn btn-primary">Go Home</a>
</div>
{% endblock %}''',

    'about.html': '''{% extends "base.html" %}
{% block title %}About{% endblock %}
{% block content %}
<h2>About Campus Resource Hub</h2>
<p class="lead">A comprehensive platform for sharing and managing campus resources.</p>
<p>This application was developed as part of the MSIS Core AiDD 2025 Capstone Project.</p>
{% endblock %}''',

    'help.html': '''{% extends "base.html" %}
{% block title %}Help{% endblock %}
{% block content %}
<h2>Help & FAQ</h2>
<div class="accordion" id="faqAccordion">
    <div class="accordion-item">
        <h2 class="accordion-header">
            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#faq1">
                How do I book a resource?
            </button>
        </h2>
        <div id="faq1" class="accordion-collapse collapse show">
            <div class="accordion-body">
                Browse available resources, select one, and click "Book Now" to make a reservation.
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
}

def create_templates():
    """Create all template files."""
    for path, content in TEMPLATES.items():
        full_path = os.path.join(VIEWS_DIR, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {path}")

if __name__ == '__main__':
    create_templates()
    print("All templates created successfully!")
