"""
ER Diagram Generator for Campus Resource Hub
Generates a visual Entity-Relationship diagram from the database models
"""

import os

# ASCII-based ER diagram (can be converted to PNG using online tools or graphviz)
ER_DIAGRAM_ASCII = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                     CAMPUS RESOURCE HUB - ER DIAGRAM                         │
└──────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│       USER          │
│─────────────────────│
│ PK id (INT)         │◄───────┐
│    username         │        │
│    email (UNIQUE)   │        │ 1:N (creator)
│    password_hash    │        │
│    role (ENUM)      │        │
│    department       │        │
│    created_at       │        │
│    google_token     │        │
│    google_refresh   │        │
└─────────────────────┘        │
         │                     │
         │ 1:N (owner)         │
         │                     │
         ▼                     │
┌─────────────────────┐        │
│     RESOURCE        │◄───────┤
│─────────────────────│        │
│ PK id (INT)         │        │ 1:N (author)
│ FK owner_id         │        │
│    title            │        │
│    description      │        │
│    category         │        │
│    location         │        │
│    capacity         │        │
│    images (JSON)    │        │
│    equipment (JSON) │        │
│    status (ENUM)    │        │
│    approval_req     │        │
│    created_at       │        │
└─────────────────────┘        │
         │                     │
         │ 1:N (resource)      │
         │                     │
         ▼                     │
┌─────────────────────┐        │
│      BOOKING        │◄───────┤
│─────────────────────│        │
│ PK id (INT)         │        │
│ FK resource_id      │        │
│ FK user_id          │◄───────┘ 1:N (user)
│    start_time       │
│    end_time         │
│    status (ENUM)    │
│    purpose          │
│    notes            │
│    created_at       │
│    google_event_id  │
└─────────────────────┘
         │ 1:1
         │
         ▼
┌─────────────────────┐
│      REVIEW         │
│─────────────────────│
│ PK id (INT)         │
│ FK resource_id      │───┐
│ FK user_id          │   │ 1:N (resource)
│ FK booking_id       │   │
│    rating (1-5)     │   │
│    comment          │   │
│    created_at       │   │
└─────────────────────┘   │
                          │
                          └──────┐
┌─────────────────────┐          │
│      MESSAGE        │          │
│─────────────────────│          │
│ PK id (INT)         │          │
│ FK sender_id        │──────────┤
│ FK receiver_id      │          │ M:N (users)
│ FK booking_id       │          │
│    subject          │          │
│    body             │          │
│    is_read          │          │
│    created_at       │          │
└─────────────────────┘          │
                                 │
┌─────────────────────┐          │
│     ADMIN_LOG       │          │
│─────────────────────│          │
│ PK id (INT)         │          │
│ FK admin_id         │──────────┘
│    action_type      │
│    target_type      │
│    target_id        │
│    description      │
│    ip_address       │
│    created_at       │
└─────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
RELATIONSHIP LEGEND
═══════════════════════════════════════════════════════════════════════════════

Symbol Meanings:
  PK = Primary Key
  FK = Foreign Key
  1:N = One-to-Many relationship
  1:1 = One-to-One relationship
  M:N = Many-to-Many relationship
  ───► = Foreign Key relationship direction

Key Relationships:
  1. USER ───► RESOURCE (owner_id)
     - One user can own many resources
     - Each resource has exactly one owner

  2. USER ───► BOOKING (user_id)
     - One user can make many bookings
     - Each booking belongs to one user

  3. RESOURCE ───► BOOKING (resource_id)
     - One resource can have many bookings
     - Each booking is for one resource

  4. BOOKING ───► REVIEW (booking_id)
     - One booking can have one review
     - Each review is for one booking

  5. USER ───► REVIEW (user_id)
     - One user can write many reviews
     - Each review is written by one user

  6. RESOURCE ───► REVIEW (resource_id)
     - One resource can have many reviews
     - Each review is for one resource

  7. USER ───► MESSAGE (sender_id, receiver_id)
     - One user can send/receive many messages
     - Each message has one sender and one receiver

  8. BOOKING ───► MESSAGE (booking_id) [optional]
     - Messages can be linked to bookings
     - One booking can have many related messages

  9. USER ───► ADMIN_LOG (admin_id)
     - One admin can create many log entries
     - Each log entry is created by one admin

═══════════════════════════════════════════════════════════════════════════════
DATABASE CONSTRAINTS & INDEXES
═══════════════════════════════════════════════════════════════════════════════

UNIQUE CONSTRAINTS:
  - users.email (UNIQUE)
  - users.username (UNIQUE)

INDEXES:
  - resources.category
  - resources.status
  - bookings.start_time
  - bookings.end_time
  - bookings.status
  - messages.is_read
  - admin_logs.action_type
  - admin_logs.created_at

CASCADE DELETES:
  - Delete USER → Delete all RESOURCES (owned)
  - Delete USER → Delete all BOOKINGS (made)
  - Delete USER → Delete all REVIEWS (written)
  - Delete USER → Delete all MESSAGES (sent/received)
  - Delete USER → Delete all ADMIN_LOGS (created)
  - Delete RESOURCE → Delete all BOOKINGS (for resource)
  - Delete RESOURCE → Delete all REVIEWS (for resource)
  - Delete BOOKING → Set MESSAGE.booking_id to NULL (optional link)
  - Delete BOOKING → Delete associated REVIEW

ENUMERATIONS:
  - users.role: ['student', 'staff', 'admin']
  - resources.status: ['draft', 'published', 'archived']
  - resources.category: ['study_room', 'lab', 'equipment', 'event_space', 'other']
  - bookings.status: ['pending', 'approved', 'rejected', 'cancelled']
  - admin_logs.action_type: ['create', 'update', 'delete', 'approve', 'reject']
  - admin_logs.target_type: ['user', 'resource', 'booking', 'review']

═══════════════════════════════════════════════════════════════════════════════
TECHNICAL NOTES
═══════════════════════════════════════════════════════════════════════════════

1. All timestamps are stored with timezone information (TIMESTAMP WITH TIME ZONE)
2. JSON fields (images, equipment) store arrays of strings
3. Password hashes use bcrypt with 12 rounds
4. Google OAuth tokens encrypted at rest
5. Foreign keys enforce referential integrity
6. Cascade deletes prevent orphaned records
7. Default values provided for created_at (CURRENT_TIMESTAMP)
8. Check constraints ensure rating is between 1-5
9. Booking conflict prevention handled at application layer
10. Audit logs immutable (no UPDATE or DELETE allowed)

═══════════════════════════════════════════════════════════════════════════════
"""

def generate_mermaid_erd():
    """Generate Mermaid ER diagram code (can be rendered on GitHub or mermaid.live)"""
    return """```mermaid
erDiagram
    USER ||--o{ RESOURCE : "owns"
    USER ||--o{ BOOKING : "makes"
    USER ||--o{ REVIEW : "writes"
    USER ||--o{ MESSAGE : "sends"
    USER ||--o{ MESSAGE : "receives"
    USER ||--o{ ADMIN_LOG : "creates"
    
    RESOURCE ||--o{ BOOKING : "has"
    RESOURCE ||--o{ REVIEW : "receives"
    
    BOOKING ||--o| REVIEW : "gets"
    BOOKING ||--o{ MESSAGE : "relates_to"

    USER {
        int id PK
        string username UNIQUE
        string email UNIQUE
        string password_hash
        enum role
        string department
        datetime created_at
        string google_token
        string google_refresh_token
    }

    RESOURCE {
        int id PK
        int owner_id FK
        string title
        text description
        enum category
        string location
        int capacity
        json images
        json equipment
        enum status
        boolean approval_required
        datetime created_at
    }

    BOOKING {
        int id PK
        int resource_id FK
        int user_id FK
        datetime start_time
        datetime end_time
        enum status
        string purpose
        text notes
        datetime created_at
        string google_event_id
    }

    REVIEW {
        int id PK
        int resource_id FK
        int user_id FK
        int booking_id FK
        int rating
        text comment
        datetime created_at
    }

    MESSAGE {
        int id PK
        int sender_id FK
        int receiver_id FK
        int booking_id FK
        string subject
        text body
        boolean is_read
        datetime created_at
    }

    ADMIN_LOG {
        int id PK
        int admin_id FK
        enum action_type
        enum target_type
        int target_id
        text description
        string ip_address
        datetime created_at
    }
```"""

def main():
    """Generate and save ER diagrams in multiple formats"""
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    # Save ASCII diagram
    ascii_path = os.path.join(docs_dir, 'ER_Diagram_ASCII.txt')
    with open(ascii_path, 'w', encoding='utf-8') as f:
        f.write(ER_DIAGRAM_ASCII)
    print(f"✓ ASCII ER diagram saved to: {ascii_path}")
    
    # Save Mermaid diagram
    mermaid_path = os.path.join(docs_dir, 'ER_Diagram_Mermaid.md')
    with open(mermaid_path, 'w', encoding='utf-8') as f:
        f.write("# Campus Resource Hub - Entity Relationship Diagram\n\n")
        f.write("## Mermaid ER Diagram\n\n")
        f.write("This diagram can be rendered on GitHub or at https://mermaid.live\n\n")
        f.write(generate_mermaid_erd())
    print(f"✓ Mermaid ER diagram saved to: {mermaid_path}")
    
    print("\n" + "="*80)
    print("ER DIAGRAM GENERATION COMPLETE")
    print("="*80)
    print("\nNext Steps:")
    print("1. View ASCII diagram: Open docs/ER_Diagram_ASCII.txt")
    print("2. Render Mermaid diagram:")
    print("   - Push to GitHub (renders automatically)")
    print("   - Or visit https://mermaid.live and paste the code")
    print("3. To generate PNG:")
    print("   - Use Mermaid Live Editor export")
    print("   - Or install: npm install -g @mermaid-js/mermaid-cli")
    print("   - Then run: mmdc -i docs/ER_Diagram_Mermaid.md -o docs/ER_Diagram.png")

if __name__ == '__main__':
    main()
