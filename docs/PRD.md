# Product Requirements Document (PRD)
## Campus Resource Hub

**Version**: 1.0  
**Date**: November 11, 2025  
**Project**: MSIS Core AiDD 2025 Capstone  
**Team**: Core Team

---

## 1. Executive Summary

Campus Resource Hub is a comprehensive web platform designed to streamline the discovery, sharing, and booking of campus resources at universities. The platform addresses the inefficiency and fragmentation in how students, staff, and faculty access shared resources such as study rooms, equipment, lab instruments, and event spaces.

**Objective**: Create a centralized, user-friendly system that increases resource utilization, reduces booking conflicts, and improves the overall campus experience.

**Target Users**:
- Students seeking study spaces and equipment
- Faculty requiring specialized lab equipment
- Staff managing departmental resources
- Administrators overseeing campus resource allocation

---

## 2. Problem Statement

### Current Challenges
1. **Fragmented Systems**: Resources are managed across multiple platforms, spreadsheets, and manual processes
2. **Booking Conflicts**: No centralized system to prevent double-bookings
3. **Discovery Issues**: Students and staff struggle to find available resources
4. **Lack of Accountability**: No rating system or usage tracking
5. **Communication Gaps**: Difficult to coordinate with resource owners

### Impact
- Underutilization of expensive equipment and facilities
- Lost productivity due to booking conflicts
- Poor user experience leading to decreased engagement
- Administrative burden from manual conflict resolution

---

## 3. Solution Overview

Campus Resource Hub provides:
- **Centralized Resource Directory**: Single source of truth for all campus resources
- **Intelligent Booking System**: Real-time availability with conflict prevention
- **Communication Tools**: Direct messaging between users and resource owners
- **Quality Control**: Rating and review system for accountability
- **Administrative Oversight**: Comprehensive management and analytics tools
- **Calendar Integration**: Sync with Google Calendar and export to iCal

---

## 4. Core Features

### 4.1 User Management & Authentication
- **Registration**: Self-service account creation with email verification
- **Role-Based Access**: Three tiers (Student, Staff, Admin) with appropriate permissions
- **Profile Management**: Editable user profiles with department affiliation
- **Security**: bcrypt password hashing, session management, CSRF protection

**Success Metric**: 90% of target users create accounts within first month

### 4.2 Resource Management
- **Resource Creation**: Staff and approved users can list resources
- **Rich Metadata**: Title, description, category, location, capacity, equipment list
- **Image Gallery**: Multiple image uploads per resource
- **Lifecycle States**: Draft, Published, Archived
- **Approval Requirements**: Optional admin approval for bookings

**Success Metric**: 100+ resources listed within first semester

### 4.3 Search & Discovery
- **Full-Text Search**: Search across titles and descriptions
- **Advanced Filters**: Category, location, capacity, availability
- **Sort Options**: Recent, most booked, top-rated
- **Google Search Integration**: Enhanced discovery using Custom Search API

**Success Metric**: Users find relevant resources within 30 seconds

### 4.4 Booking System
- **Calendar Interface**: Date and time selection with visual availability
- **Conflict Detection**: Real-time validation against existing bookings
- **Approval Workflow**: Automatic or manual approval based on resource settings
- **Notifications**: Email/message alerts for status changes
- **Calendar Sync**: Google Calendar OAuth integration
- **iCal Export**: Universal calendar format for all calendar apps

**Success Metric**: 95% of bookings completed without conflicts

### 4.5 Communication
- **Direct Messaging**: User-to-user threaded conversations
- **Booking Context**: Messages linked to specific bookings
- **Unread Indicators**: Visual cues for new messages
- **Notification System**: Automated messages for booking events

**Success Metric**: 80% of booking questions resolved through messaging

### 4.6 Reviews & Ratings
- **Post-Booking Reviews**: Only users with completed bookings can review
- **5-Star Rating System**: Standardized quality metric
- **Text Reviews**: Detailed feedback and recommendations
- **Aggregate Ratings**: Average scores and rating distribution
- **Moderation Tools**: Admin ability to hide inappropriate reviews

**Success Metric**: 60% of completed bookings receive reviews

### 4.7 Admin Dashboard
- **User Management**: View, edit, suspend user accounts
- **Resource Oversight**: Monitor and moderate all listings
- **Booking Management**: View and modify bookings, resolve conflicts
- **Review Moderation**: Hide inappropriate content
- **Analytics**: Usage statistics, popular resources, user engagement
- **Audit Logs**: Comprehensive tracking of all administrative actions

**Success Metric**: Admin resolves 95% of issues within 24 hours

---

## 5. Advanced Features

### 5.1 Google Custom Search API
- **Enhanced Discovery**: Search beyond local database
- **External Resources**: Find related campus resources from university websites
- **Intelligent Suggestions**: Recommend similar resources

### 5.2 Google Calendar Integration
- **OAuth 2.0 Flow**: Secure authorization with user consent
- **Two-Way Sync**: Bookings automatically added to Google Calendar
- **Automatic Reminders**: Leverage Google Calendar notification system
- **Token Management**: Secure storage and refresh of access tokens

### 5.3 iCal Export
- **Individual Export**: Download single booking as .ics file
- **Bulk Export**: All user bookings in one calendar file
- **Universal Compatibility**: Works with Outlook, Apple Calendar, Google Calendar

---

## 6. User Personas

### Persona 1: Alex - Undergraduate Student
- **Goal**: Find quiet study rooms for group projects
- **Pain Points**: Study rooms always booked, no visibility into availability
- **How Campus Hub Helps**: Real-time search, easy booking, calendar integration

### Persona 2: Dr. Martinez - Faculty Researcher
- **Goal**: Reserve lab equipment for experiments
- **Pain Points**: Equipment booking is manual, conflicts common
- **How Campus Hub Helps**: Equipment tracking, approval workflows, usage history

### Persona 3: Jamie - Staff Facilities Manager
- **Goal**: Manage departmental resources efficiently
- **Pain Points**: Too many spreadsheets, no oversight
- **How Campus Hub Helps**: Admin dashboard, analytics, audit trails

---

## 7. Success Metrics (OKRs)

### Objective 1: Drive User Adoption
- **KR1**: 500 registered users in first semester
- **KR2**: 70% monthly active user rate
- **KR3**: Average of 3 bookings per active user per month

### Objective 2: Improve Resource Utilization
- **KR1**: 30% increase in booking frequency
- **KR2**: 95% reduction in double-booking incidents
- **KR3**: 85% of resources booked at least once per month

### Objective 3: Enhance User Experience
- **KR1**: 4.5+ average rating for platform usability
- **KR2**: 90% successful booking rate (no conflicts)
- **KR3**: <2 minutes average time from search to booking submission

---

## 8. Non-Goals

**Explicitly Out of Scope**:
- Payment processing or resource rentals
- Complex recurring booking patterns (e.g., semester-long reservations)
- Integration with university ERP/SIS systems
- Mobile native applications (responsive web only)
- Real-time video conferencing
- Third-party marketplace for off-campus resources

---

## 9. Technical Requirements

### Performance
- Page load time <2 seconds
- Booking conflict check <500ms
- Support 100 concurrent users

### Security
- OWASP Top 10 compliance
- Data encryption in transit (HTTPS)
- Secure password storage (bcrypt)
- Input validation and sanitization
- CSRF and XSS protection

### Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader compatibility
- Sufficient color contrast ratios

### Browser Support
- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)

---

## 10. Dependencies & Assumptions

### Dependencies
- Google Cloud Platform (Calendar API, Custom Search API)
- Email service for notifications (SMTP or SendGrid)
- Web hosting with Python 3.10+ support
- Domain name and SSL certificate

### Assumptions
- Users have access to email for account verification
- University allows Google OAuth integration
- Staff are willing to migrate from existing systems
- Basic computer literacy among target users

---

## 11. Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Low user adoption | Medium | High | Conduct user testing, provide training sessions |
| Google API rate limits | Low | Medium | Implement caching, monitor usage |
| Data privacy concerns | Low | High | Clear privacy policy, GDPR compliance |
| System downtime | Medium | Medium | Automated backups, monitoring alerts |
| Booking conflicts despite validation | Low | High | Comprehensive testing, database locks |

---

## 12. Stakeholder Map

- **Primary Stakeholders**: Students, Faculty, Staff
- **Secondary Stakeholders**: Department Heads, IT Administrators
- **Executive Sponsors**: University Dean, CIO
- **Development Team**: Core Team (4 members)
- **End Users**: 10,000+ campus community members

---

## 13. Timeline & Milestones

| Milestone | Date | Deliverable |
|-----------|------|-------------|
| Project Kickoff | Oct 28, 2025 | Requirements finalized |
| MVP Completed | Nov 8, 2025 | Core features functional |
| Testing & QA | Nov 10-12, 2025 | Test suite passing |
| Documentation | Nov 13-14, 2025 | README, PRD, API docs |
| **Final Submission** | **Nov 15, 2025** | **Complete application** |
| Demo Presentation | Nov 18, 2025 | Live demonstration |

---

## 14. Future Enhancements (Post-MVP)

**Phase 2 (Semester 2)**:
- Mobile native applications (iOS, Android)
- SMS notifications
- Advanced analytics with data visualization
- API for third-party integrations
- Waitlist functionality for fully booked resources

**Phase 3 (Year 2)**:
- AI-powered resource recommendations
- Predictive booking suggestions
- Integration with university identity management
- Multi-campus support
- Resource usage forecasting

---

## Approval & Sign-Off

**Product Lead**: _________________________ Date: _________

**Technical Lead**: _________________________ Date: _________

**Quality Lead**: _________________________ Date: _________

**Instructor Approval**: _________________________ Date: _________

---

**Document Control**:
- Version: 1.0
- Last Updated: November 11, 2025
- Next Review: Post-Demo (November 18, 2025)
