# Customer Care System - PostgreSQL Integration

## Overview
A complete customer care management system has been integrated with PostgreSQL backend to handle customer issues, complaints, and support management.

## Database Model
**Table:** `customer_care`

```sql
- id: Integer (Primary Key)
- name: String(255) - Customer name
- email: String(255) - Customer email
- phone: String(20) - Customer phone
- order_id: String(100) - Related order ID (optional)
- issue_type: String(100) - Type of issue
- description: Text - Detailed description
- priority: String(20) - Priority level (normal/high/urgent)
- status: String(50) - Status (open/in-progress/resolved)
- created_at: DateTime - When issue was created
- updated_at: DateTime - When issue was last updated
- admin_response: Text - Admin's response to the issue
- resolved_at: DateTime - When issue was resolved
```

## Backend Features

### Database Functions (models.py)
- `add_customer_care_issue()` - Add new issue to database
- `get_all_customer_care_issues()` - Retrieve all issues
- `get_customer_care_issue_by_id()` - Get specific issue
- `get_customer_care_issues_by_status()` - Filter by status
- `get_customer_care_issues_by_priority()` - Filter by priority
- `update_customer_care_issue()` - Update issue status/response
- `delete_customer_care_issue()` - Delete an issue
- `get_customer_care_count()` - Total issue count
- `get_open_customer_care_count()` - Count of open issues

### API Endpoints (app.py)

#### Customer Endpoints
1. **GET /customer-care**
   - Display customer care page with form

2. **POST /api/customer-care/report**
   - Submit a new customer care issue
   - Body: `{name, email, phone, issue_type, description, order_id, priority}`
   - Returns: Issue ID and success message

#### Admin Endpoints
1. **GET /admin/customer-care**
   - Dashboard showing all customer care issues
   - Includes filtering and search functionality

2. **GET /admin/customer-care/<issue_id>**
   - View detailed issue information

3. **POST /api/admin/customer-care/<issue_id>/respond**
   - Admin responds to customer issue
   - Body: `{response, status}`
   - Updates status and adds admin response

4. **POST /api/admin/customer-care/<issue_id>/delete**
   - Delete a customer care issue

## Frontend Templates

### Customer Pages
**`templates/customer_care.html`**
- Public customer care page
- Form to report issues
- Support channels information (Phone, WhatsApp, Email)
- Shop hours
- FAQs with collapsible accordion
- Form submission with validation and toast notifications

### Admin Pages
**`templates/admin/customer_care.html`**
- Dashboard for all customer care issues
- Real-time search by name/email/phone
- Filter by status (Open/In Progress/Resolved)
- Filter by priority (Normal/High/Urgent)
- Issue table with key information
- Quick action buttons

**`templates/admin/customer_care_detail.html`**
- Detailed view of individual issue
- Customer information display
- Issue details section
- Admin response form
- Quick contact buttons (Call/WhatsApp/Email)
- Timeline of issue lifecycle
- Delete functionality

## Issue Types Supported
1. **not_received** - Order Not Received (📦)
2. **quality** - Product Quality Issue (⚠️)
3. **wrong_item** - Wrong Item Delivered (❌)
4. **damaged** - Damaged Packaging (💔)
5. **payment** - Payment Issues (💳)
6. **refund** - Refund/Return Query (💰)
7. **app** - App/Website Issues (📱)
8. **other** - Other Issues (❓)

## Priority Levels
- **normal** - Normal priority (🔵)
- **high** - High priority (🟠)
- **urgent** - Urgent priority (🔴)

## Issue Status
- **open** - New issue (🔴)
- **in-progress** - Being handled (🟡)
- **resolved** - Issue resolved (🟢)

## How to Use

### For Customers
1. Visit `/customer-care` page
2. Fill out the form with issue details
3. Submit the form
4. System stores issue in PostgreSQL database
5. Admin will respond within 24 hours

### For Admin
1. Go to Admin Panel → Customer Care
2. View all issues with filtering options
3. Click on an issue to view details
4. Send response to customer
5. Update status to In Progress or Resolved
6. Option to delete resolved issues

## Database Migration
Migration file created: `migrations/versions/`
- Table automatically created with proper indexes
- All relationships properly defined

## Integration Points
- PostgreSQL database for persistent storage
- Flask-SQLAlchemy ORM for database operations
- Flask-Migrate for schema management
- RESTful API endpoints for frontend communication
- Toast notifications for user feedback

## Security Features
- Admin login required for management pages
- Data validation on form submission
- Proper error handling and messages
- SQL injection prevention via ORM

## Features Implemented
✅ Customer can report issues from website
✅ All data stored in PostgreSQL database
✅ Admin dashboard for issue management
✅ Real-time search and filtering
✅ Admin response tracking
✅ Issue status management
✅ Priority level assignment
✅ Contact customer directly (Phone/WhatsApp/Email)
✅ Issue timeline and history
✅ Delete resolved issues
✅ FAQ section for common issues

## Routes Summary
- `/customer-care` - Customer care page
- `/api/customer-care/report` - Submit issue API
- `/admin/customer-care` - Admin dashboard
- `/admin/customer-care/<id>` - Issue detail view
- `/api/admin/customer-care/<id>/respond` - Send response API
- `/api/admin/customer-care/<id>/delete` - Delete issue API
