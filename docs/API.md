# Campus Resource Hub - API Documentation

## Overview

This document describes the RESTful API endpoints for the Campus Resource Hub application. All endpoints follow REST conventions and return JSON responses unless otherwise specified.

**Base URL**: `http://localhost:5000` (development)  
**Authentication**: Session-based (Flask-Login)  
**Content-Type**: `application/json` or `application/x-www-form-urlencoded`

---

## Authentication

All protected endpoints require an authenticated session. If not authenticated, the API will return a 401 Unauthorized response or redirect to the login page.

### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

email=user@example.com&password=secret&csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /dashboard
```

### Logout
```http
GET /auth/logout
```

**Response** (302 Redirect):
```
Location: /
```

### Register
```http
POST /auth/register
Content-Type: application/x-www-form-urlencoded

username=johndoe&email=john@example.com&password=secret&confirm_password=secret&role=student&department=Computer Science&csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /auth/login
```

---

## Resources

### List Resources
```http
GET /resources
```

**Query Parameters**:
- `category` (optional): Filter by category (study_room, lab, equipment, event_space)
- `search` (optional): Search term for title/description
- `location` (optional): Filter by location
- `page` (optional): Page number for pagination (default: 1)

**Response** (HTML):
```html
<!-- Rendered resources/list.html template -->
```

### Get Resource Details
```http
GET /resources/<int:id>
```

**Response** (HTML):
```html
<!-- Rendered resources/detail.html template with resource data, reviews, availability calendar -->
```

### Create Resource
```http
POST /resources/create
Content-Type: multipart/form-data
Authentication: Required (Staff or Admin)

title=Science Lab A
description=Fully equipped lab
category=lab
location=Building 5, Room A
capacity=20
equipment=Microscopes, Bunsen Burners
images=@file1.jpg,@file2.jpg
approval_required=true
status=published
csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /resources/<new_id>
```

### Update Resource
```http
POST /resources/<int:id>/edit
Content-Type: multipart/form-data
Authentication: Required (Owner or Admin)

title=Updated Title
description=Updated description
[... other fields ...]
csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /resources/<id>
```

### Delete Resource
```http
POST /resources/<int:id>/delete
Authentication: Required (Owner or Admin)

csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /resources
```

---

## Bookings

### List User Bookings
```http
GET /bookings/my-bookings
Authentication: Required
```

**Response** (HTML):
```html
<!-- Rendered bookings/my_bookings.html with user's bookings -->
```

### Create Booking
```http
POST /bookings/create
Content-Type: application/x-www-form-urlencoded
Authentication: Required

resource_id=5
start_time=2025-12-15T14:00
end_time=2025-12-15T16:00
purpose=Research experiment
notes=Need microscope setup
csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /bookings/<new_id>
```

**Error Response** (Conflict):
```json
{
  "error": "Booking conflict exists for the selected time slot"
}
```

### Check Availability (AJAX)
```http
GET /bookings/check-availability
Authentication: Required

?resource_id=5&start_time=2025-12-15T14:00&end_time=2025-12-15T16:00
```

**Response** (JSON):
```json
{
  "available": false,
  "conflicts": [
    {
      "id": 123,
      "start_time": "2025-12-15T13:00:00",
      "end_time": "2025-12-15T15:00:00",
      "user": "John Doe"
    }
  ]
}
```

### Approve Booking
```http
POST /bookings/<int:id>/approve
Authentication: Required (Resource Owner or Admin)

csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /bookings/<id>
```

### Reject Booking
```http
POST /bookings/<int:id>/reject
Authentication: Required (Resource Owner or Admin)

reason=Resource not available
csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /bookings/<id>
```

### Cancel Booking
```http
POST /bookings/<int:id>/cancel
Authentication: Required (Booking Owner)

csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /bookings/my-bookings
```

---

## Messages

### Inbox
```http
GET /messages/inbox
Authentication: Required
```

**Query Parameters**:
- `filter` (optional): Filter by message type (all, unread, booking, reviews, general)
- `page` (optional): Page number

**Response** (HTML):
```html
<!-- Rendered messages/inbox.html with message list -->
```

### View Thread
```http
GET /messages/thread/<int:message_id>
Authentication: Required
```

**Response** (HTML):
```html
<!-- Rendered messages/thread.html with full conversation -->
```

### Send Message
```http
POST /messages/send
Content-Type: application/x-www-form-urlencoded
Authentication: Required

receiver_id=10
subject=Booking Question
body=Is the lab available earlier?
booking_id=5
csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /messages/thread/<new_message_id>
```

### Reply to Message
```http
POST /messages/reply/<int:message_id>
Content-Type: application/x-www-form-urlencoded
Authentication: Required

body=Yes, you can come at 1 PM instead
csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /messages/thread/<message_id>
```

---

## Reviews

### Create Review
```http
POST /reviews/create
Content-Type: application/x-www-form-urlencoded
Authentication: Required

resource_id=5
booking_id=10
rating=5
comment=Excellent facilities, very clean
csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /resources/<resource_id>
```

**Business Rules**:
- User must have a completed booking for the resource
- One review per booking
- Rating must be 1-5

### Update Review
```http
POST /reviews/<int:id>/edit
Content-Type: application/x-www-form-urlencoded
Authentication: Required (Review Author)

rating=4
comment=Updated review text
csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /resources/<resource_id>
```

### Delete Review
```http
POST /reviews/<int:id>/delete
Authentication: Required (Review Author or Admin)

csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /resources/<resource_id>
```

---

## Calendar Integration

### Connect Google Calendar
```http
GET /calendar/authorize
Authentication: Required
```

**Response** (302 Redirect):
```
Location: https://accounts.google.com/o/oauth2/auth?...
```

### OAuth Callback
```http
GET /calendar/oauth2callback
Authentication: Required

?state=<state_token>&code=<auth_code>
```

**Response** (302 Redirect):
```
Location: /auth/profile
```

### Sync Booking to Google Calendar
```http
POST /calendar/sync/<int:booking_id>
Authentication: Required

csrf_token=xyz
```

**Response** (JSON):
```json
{
  "success": true,
  "event_id": "abc123xyz",
  "message": "Booking synced to Google Calendar"
}
```

### Export Booking as iCal
```http
GET /calendar/export/<int:booking_id>
Authentication: Required
```

**Response** (File Download):
```
Content-Type: text/calendar
Content-Disposition: attachment; filename="booking_<id>.ics"

BEGIN:VCALENDAR
VERSION:2.0
...
END:VCALENDAR
```

### Export All Bookings as iCal
```http
GET /calendar/export-all
Authentication: Required
```

**Response** (File Download):
```
Content-Type: text/calendar
Content-Disposition: attachment; filename="my_bookings.ics"

BEGIN:VCALENDAR
VERSION:2.0
...
END:VCALENDAR
```

### Disconnect Google Calendar
```http
POST /calendar/disconnect
Authentication: Required

csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /auth/profile
```

---

## Search

### Basic Search
```http
GET /search
```

**Query Parameters**:
- `q`: Search query
- `category`: Filter by category
- `location`: Filter by location
- `min_capacity`: Minimum capacity
- `max_capacity`: Maximum capacity
- `sort`: Sort order (recent, popular, rating)
- `page`: Page number

**Response** (HTML):
```html
<!-- Rendered search.html with results -->
```

### Google Custom Search (Advanced)
```http
GET /search/google
Authentication: Required
```

**Query Parameters**:
- `q`: Search query

**Response** (JSON):
```json
{
  "results": [
    {
      "title": "Campus Resource from University Site",
      "link": "https://university.edu/resources/lab-a",
      "snippet": "Description of external resource..."
    }
  ],
  "count": 10
}
```

---

## Admin Panel

All admin endpoints require `admin` role authentication.

### Admin Dashboard
```http
GET /admin
Authentication: Required (Admin)
```

**Response** (HTML):
```html
<!-- Rendered admin/dashboard.html with statistics -->
```

### Manage Users
```http
GET /admin/users
Authentication: Required (Admin)
```

**Query Parameters**:
- `search`: Search by username/email
- `role`: Filter by role
- `page`: Page number

**Response** (HTML):
```html
<!-- Rendered admin/users.html with user list -->
```

### Edit User
```http
POST /admin/users/<int:id>/edit
Authentication: Required (Admin)

username=newusername
role=staff
is_active=true
csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /admin/users
```

### Delete User
```http
POST /admin/users/<int:id>/delete
Authentication: Required (Admin)

csrf_token=xyz
```

**Response** (302 Redirect):
```
Location: /admin/users
```

### View Audit Logs
```http
GET /admin/logs
Authentication: Required (Admin)
```

**Query Parameters**:
- `action_type`: Filter by action (create, update, delete, approve, reject)
- `target_type`: Filter by target (user, resource, booking, review)
- `admin_id`: Filter by admin user
- `page`: Page number

**Response** (HTML):
```html
<!-- Rendered admin/logs.html with audit trail -->
```

### Analytics
```http
GET /admin/analytics
Authentication: Required (Admin)
```

**Response** (HTML):
```html
<!-- Rendered admin/analytics.html with charts and statistics -->
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input",
  "message": "End time must be after start time"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required",
  "message": "Please log in to access this resource"
}
```

### 403 Forbidden
```json
{
  "error": "Access denied",
  "message": "You do not have permission to perform this action"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "message": "The requested resource does not exist"
}
```

### 409 Conflict
```json
{
  "error": "Booking conflict",
  "message": "A booking already exists for this time slot"
}
```

### 500 Internal Server Error
```json
{
  "error": "Server error",
  "message": "An unexpected error occurred. Please try again later."
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, consider:
- 100 requests per minute per IP for public endpoints
- 1000 requests per hour per authenticated user
- 10 login attempts per hour per IP

---

## Webhooks (Future Enhancement)

Not yet implemented. Future versions may support:
- Booking status change webhooks
- New message notifications
- Review submission notifications

---

## Data Models

### User
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "role": "student",
  "department": "Computer Science",
  "created_at": "2025-11-01T10:00:00Z",
  "google_calendar_connected": true
}
```

### Resource
```json
{
  "id": 5,
  "title": "Science Lab A",
  "description": "Fully equipped lab...",
  "category": "lab",
  "location": "Building 5, Room A",
  "capacity": 20,
  "images": ["img1.jpg", "img2.jpg"],
  "equipment": ["Microscopes", "Bunsen Burners"],
  "status": "published",
  "approval_required": true,
  "owner": {
    "id": 10,
    "username": "drsmith"
  },
  "average_rating": 4.8,
  "review_count": 24,
  "created_at": "2025-10-15T12:00:00Z"
}
```

### Booking
```json
{
  "id": 123,
  "resource_id": 5,
  "user_id": 1,
  "start_time": "2025-12-15T14:00:00Z",
  "end_time": "2025-12-15T16:00:00Z",
  "status": "approved",
  "purpose": "Research experiment",
  "notes": "Need microscope setup",
  "google_event_id": "abc123xyz",
  "created_at": "2025-12-01T09:00:00Z"
}
```

### Review
```json
{
  "id": 50,
  "resource_id": 5,
  "user_id": 1,
  "booking_id": 123,
  "rating": 5,
  "comment": "Excellent facilities!",
  "created_at": "2025-12-16T10:00:00Z",
  "user": {
    "username": "johndoe"
  }
}
```

### Message
```json
{
  "id": 200,
  "sender_id": 1,
  "receiver_id": 10,
  "subject": "Booking Question",
  "body": "Is the lab available earlier?",
  "is_read": false,
  "booking_id": 123,
  "created_at": "2025-12-10T15:00:00Z",
  "sender": {
    "username": "johndoe"
  },
  "receiver": {
    "username": "drsmith"
  }
}
```

---

## CORS Configuration

Currently, CORS is not configured as this is a monolithic application. If you need to access the API from a different origin, add Flask-CORS:

```python
from flask_cors import CORS

app = create_app()
CORS(app, origins=["https://yourdomain.com"])
```

---

## API Versioning

Current version: v1 (implicit)

Future versions may use URL versioning:
- `/api/v1/resources`
- `/api/v2/resources`

---

## Testing the API

### Using cURL
```bash
# Login
curl -X POST http://localhost:5000/auth/login \
  -d "email=user@example.com&password=secret&csrf_token=xyz" \
  -c cookies.txt

# Get resources (authenticated)
curl -X GET http://localhost:5000/resources \
  -b cookies.txt

# Check booking availability
curl -X GET "http://localhost:5000/bookings/check-availability?resource_id=5&start_time=2025-12-15T14:00&end_time=2025-12-15T16:00" \
  -b cookies.txt
```

### Using Python Requests
```python
import requests

session = requests.Session()

# Login
login_data = {
    'email': 'user@example.com',
    'password': 'secret',
    'csrf_token': 'xyz'
}
session.post('http://localhost:5000/auth/login', data=login_data)

# Check availability
params = {
    'resource_id': 5,
    'start_time': '2025-12-15T14:00',
    'end_time': '2025-12-15T16:00'
}
response = session.get('http://localhost:5000/bookings/check-availability', params=params)
print(response.json())
```

---

## Security Considerations

1. **CSRF Tokens**: All POST requests require a valid CSRF token
2. **Session Management**: Sessions expire after 31 days of inactivity
3. **Password Security**: Passwords are hashed with bcrypt (12 rounds)
4. **Input Validation**: All inputs are validated on the server side
5. **File Upload Security**: Filenames are sanitized, MIME types checked
6. **SQL Injection Prevention**: SQLAlchemy parameterized queries used throughout

---

## Support

For API issues or questions:
- GitHub Issues: [repository URL]
- Email: support@campusresourcehub.com
- Documentation: README.md

---

**Last Updated**: November 11, 2025  
**Version**: 1.0.0
