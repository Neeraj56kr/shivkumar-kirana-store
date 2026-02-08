
# Shivkumar Kirana Store 🏪

A complete full-stack web application for a village grocery shop with customer website, customer care system, chatbot, and admin panel.

**Technology**: Flask + PostgreSQL + Tailwind CSS

## ✨ Features

### 🛒 Customer Website
- Modern, mobile-first responsive design
- Product browse and search
- Shopping cart with localStorage
- Checkout with WhatsApp order integration
- Floating WhatsApp button
- AI-style chatbot for product queries

### 🤖 Chatbot
- Product availability checker
- Responds in Hindi/English
- Shows product prices and availability

### 🔐 Admin Panel
- Secure login system
- Dashboard with statistics
- Product management (Add/Edit/Delete)
- Order management
- Multi-admin support

### 💾 Production Database
- PostgreSQL database (enterprise-grade)
- Automated migrations with Flask-Migrate
- Relationships: Products, Orders, Admins, CustomerCare, ContactMessages
- Optimized queries and indexing

## 🛠️ Tech Stack

- **Backend**: Python Flask 3.0.0
- **Database**: PostgreSQL (with psycopg2)
- **ORM**: Flask-SQLAlchemy
- **Migrations**: Flask-Migrate (Alembic)
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Security**: Werkzeug password hashing
- **Templates**: Jinja2
- **WSGI Server**: Gunicorn (production)

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- Virtual Environment (recommended)

## 🚀 Installation & Setup

### 1. Clone/Download Project
```bash
cd shivkumar
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create `.env` file in project root:
```env
# Flask Configuration
SECRET_KEY=my_secret

# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://pass@localhost:5432/kirana_db

# Default Admin Credentials
ADMIN_USERNAME=neeraj
ADMIN_PASSWORD=neeraj@123
```

### 5. Initialize Database
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✅ Tables created')"
```

### 6. Run Application (Development)
```bash
python app.py
```

**Access**:
- Customer Website: http://localhost:5000
- Admin Panel: http://localhost:5000/admin

### 7. Run Application (Production)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔐 Default Admin Login

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **IMPORTANT**: Change the default password immediately after first login!

## 📁 Project Structure

```
shivkumar/
├── app.py                      # Main Flask application with all routes
├── config.py                   # Configuration and environment setup
├── models.py                   # Database models and helper functions
├── create_admin.py             # Admin account creation script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore rules
├── migrations/                 # Alembic database migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/               # Migration history
├── static/
│   └── images/
│       └── uploads/            # Product images (auto-created)
└── templates/
    ├── base.html               # Base template
    ├── index.html              # Home page
    ├── about.html              # About page
    ├── products.html           # Products listing
    ├── contact.html            # Contact form
    ├── check_reply.html        # Check replies
    ├── checkout.html           # Checkout page
    ├── my_orders.html          # My orders page
    ├── customer_care/
    │   └── index.html          # Customer Care page
    ├── 404.html                # Error page
    ├── 500.html                # Error page
    └── admin/
        ├── login.html          # Admin login
        ├── base.html           # Admin base template
        ├── dashboard.html      # Dashboard
        ├── products.html       # Product management
        ├── add_product.html    # Add product
        ├── edit_product.html   # Edit product
        ├── availability.html   # Availability management
        ├── orders.html         # Order management
        ├── customer_care.html  # Customer Care issues
        ├── customer_care_detail.html # Issue detail
        ├── contact_messages.html     # Messages list
        ├── contact_message_detail.html # Message detail
        ├── admins.html         # Admin management
        └── settings.html       # Shop settings
```

## ⚙️ Configuration

### WhatsApp Integration
Edit `templates/base.html`:
```html
<!-- Replace 919559126080 WhatsApp number -->
<a href="https://wa.me/919559126080?text=Hi...">
```

### Shop Settings
Login to Admin Panel → Settings to configure:
- Shop opening time
- Shop closing time
- Contact phone number

### Upload File Limits
- Maximum file size: 16MB
- Allowed formats: PNG, JPG, JPEG, GIF, WEBP

## 🚀 Deployment
### Render
- Create account on Render.com
- Create new Web Service
- Add PostgreSQL database
- Set environment variables

### PythonAnywhere
1. Upload files to PythonAnywhere
2. Create virtual environment
3. Configure WSGI file
4. Add environment variables

## 🔒 Security Best Practices

- ✅ Change default admin password immediately
- ✅ Use strong SECRET_KEY in production
- ✅ Store `.env` file securely (never commit to git)
- ✅ Use HTTPS in production
- ✅ Enable password hashing
- ✅ Validate all user inputs
- ✅ Regular database backups

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
# Verify DATABASE_URL in .env
# Ensure database exists
```

### Admin Login Failed
```bash
python create_admin.py
```

### Static Files Not Loading
```bash
mkdir -p static/images/uploads
```

## 📞 Support

For issues or questions, please contact the store admin.

---

**Made with neeraj for Shivkumar Kirana Store**

**Status**: Production Ready ✅
=======
# shivkumar-kirana-store
A full-stack Kirana Store Management System built with Python Flask and PostgreSQL. Features include multi-admin login, secure authentication, product management with images, order management, WhatsApp &amp; UPI integration, chatbot for product availability, and modern responsive UI. Designed for small shops and local businesses.
>>>>>>> c66a8ec9ff8f8fd85ef9254cb5e40d738b66de27
