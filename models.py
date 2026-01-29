"""
Flask-SQLAlchemy Models for Shivkumar Kirana Store
PostgreSQL with Flask-Migrate support
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ==================== Models ====================

class Product(db.Model):
    """Product model for store items."""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), default='default.png')
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'is_available': self.is_available,
            'created_at': self.created_at
        }


class Order(db.Model):
    """Order model for customer orders."""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    items = db.Column(db.Text, nullable=False)  # JSON string
    total = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default='cod')
    status = db.Column(db.String(50), default='pending')
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'mobile': self.mobile,
            'address': self.address,
            'items': self.items,
            'total': self.total,
            'payment_method': self.payment_method,
            'status': self.status,
            'date': self.date
        }


class Admin(db.Model):
    """Admin user model."""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_master = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_master': self.is_master,
            'created_at': self.created_at
        }


class Setting(db.Model):
    """Shop settings model."""
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)


class CustomerCare(db.Model):
    """Customer Care - Issues and Complaints model."""
    __tablename__ = 'customer_care'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    order_id = db.Column(db.String(100), nullable=True)
    issue_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='normal')
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_response = db.Column(db.Text, nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'order_id': self.order_id,
            'issue_type': self.issue_type,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'admin_response': self.admin_response,
            'resolved_at': self.resolved_at
        }


class ContactMessage(db.Model):
    """Contact messages from website."""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    admin_reply = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'is_read': self.is_read,
            'admin_reply': self.admin_reply,
            'created_at': self.created_at
        }


# ==================== Database Initialization ====================

def init_db(app):
    """Initialize database with app context."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        _create_default_settings()


def _create_default_settings():
    """Create default settings if not exist."""
    default_settings = [
        ('shop_open_time', '08:00'),
        ('shop_close_time', '21:00'),
        ('shop_phone', '9999999999'),
    ]
    for key, value in default_settings:
        if not Setting.query.filter_by(key=key).first():
            setting = Setting(key=key, value=value)
            db.session.add(setting)
    db.session.commit()


# ==================== Product Functions ====================

def get_all_products():
    """Get all products."""
    return Product.query.order_by(Product.id.desc()).all()


def get_product_by_id(product_id):
    """Get product by ID."""
    return Product.query.get(product_id)


def search_products(query):
    """Search products by name."""
    return Product.query.filter(Product.name.ilike(f'%{query}%')).order_by(Product.name).all()


def add_product(name, price, image='default.png'):
    """Add new product."""
    product = Product(name=name, price=price, image=image)
    db.session.add(product)
    db.session.commit()
    return product.id


def update_product(product_id, name, price, image=None):
    """Update product."""
    product = Product.query.get(product_id)
    if product:
        product.name = name
        product.price = price
        if image:
            product.image = image
        db.session.commit()


def delete_product(product_id):
    """Delete product."""
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()


def get_products_count():
    """Get total product count."""
    return Product.query.count()


def toggle_product_availability(product_id):
    """Toggle product availability."""
    product = Product.query.get(product_id)
    if product:
        product.is_available = not product.is_available
        db.session.commit()
        return product.is_available
    return None


def get_available_products():
    """Get only available products."""
    return Product.query.filter_by(is_available=True).order_by(Product.id.desc()).all()


def get_unavailable_count():
    """Get count of unavailable products."""
    return Product.query.filter_by(is_available=False).count()


# ==================== Order Functions ====================

def create_order(customer_name, mobile, address, items, total, payment_method='cod'):
    """Create new order."""
    import json
    order = Order(
        customer_name=customer_name,
        mobile=mobile,
        address=address,
        items=json.dumps(items),
        total=total,
        payment_method=payment_method
    )
    db.session.add(order)
    db.session.commit()
    return order.id


def get_all_orders():
    """Get all orders."""
    return Order.query.order_by(Order.date.desc()).all()


def get_orders_count():
    """Get total order count."""
    return Order.query.count()


def delete_order(order_id):
    """Delete order."""
    order = Order.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()


def update_order_status(order_id, status):
    """Update order status."""
    order = Order.query.get(order_id)
    if order:
        order.status = status
        db.session.commit()


def get_orders_by_mobile(mobile):
    """Get orders by mobile number."""
    return Order.query.filter_by(mobile=mobile).order_by(Order.date.desc()).all()


# ==================== Admin Functions ====================

def get_admin_by_username(username):
    """Get admin by username."""
    return Admin.query.filter_by(username=username).first()


def get_all_admins():
    """Get all admins."""
    return Admin.query.order_by(Admin.is_master.desc(), Admin.id).all()


def add_admin(username, password_hash, is_master=False):
    """Add new admin."""
    try:
        admin = Admin(username=username, password=password_hash, is_master=is_master)
        db.session.add(admin)
        db.session.commit()
        return admin.id
    except Exception:
        db.session.rollback()
        return None


def delete_admin(admin_id):
    """Delete admin if not master."""
    admin = Admin.query.get(admin_id)
    if admin and not admin.is_master:
        db.session.delete(admin)
        db.session.commit()
        return True
    return False


def is_master_admin(admin_id):
    """Check if admin is master."""
    admin = Admin.query.get(admin_id)
    return admin and admin.is_master


def get_admin_by_id(admin_id):
    """Get admin by ID."""
    return Admin.query.get(admin_id)


# ==================== Customer Care Functions ====================

def add_customer_care_issue(name, email, phone, issue_type, description, order_id=None, priority='normal'):
    """Add new customer care issue."""
    try:
        issue = CustomerCare(
            name=name,
            email=email,
            phone=phone,
            order_id=order_id,
            issue_type=issue_type,
            description=description,
            priority=priority,
            status='open'
        )
        db.session.add(issue)
        db.session.commit()
        return issue.id
    except Exception as e:
        db.session.rollback()
        return None


def get_all_customer_care_issues():
    """Get all customer care issues."""
    return CustomerCare.query.order_by(CustomerCare.created_at.desc()).all()


def get_customer_care_issue_by_id(issue_id):
    """Get customer care issue by ID."""
    return CustomerCare.query.get(issue_id)


def get_customer_care_issues_by_status(status):
    """Get customer care issues by status."""
    return CustomerCare.query.filter_by(status=status).order_by(CustomerCare.created_at.desc()).all()


def get_customer_care_issues_by_priority(priority):
    """Get customer care issues by priority."""
    return CustomerCare.query.filter_by(priority=priority).order_by(CustomerCare.created_at.desc()).all()


def update_customer_care_issue(issue_id, status=None, admin_response=None, resolved_at=None):
    """Update customer care issue."""
    issue = CustomerCare.query.get(issue_id)
    if issue:
        if status:
            issue.status = status
        if admin_response:
            issue.admin_response = admin_response
        if resolved_at:
            issue.resolved_at = resolved_at
        db.session.commit()
        return True
    return False


def delete_customer_care_issue(issue_id):
    """Delete customer care issue."""
    issue = CustomerCare.query.get(issue_id)
    if issue:
        db.session.delete(issue)
        db.session.commit()
        return True
    return False


def get_customer_care_count():
    """Get total count of customer care issues."""
    return CustomerCare.query.count()


def get_open_customer_care_count():
    """Get count of open customer care issues."""
    return CustomerCare.query.filter_by(status='open').count()


# ==================== Contact Message Functions ====================

def add_contact_message(name, email, message):
    """Add new contact message."""
    try:
        msg = ContactMessage(name=name, email=email, message=message)
        db.session.add(msg)
        db.session.commit()
        return msg.id
    except Exception:
        db.session.rollback()
        return None


def get_all_contact_messages():
    """Get all contact messages."""
    return ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()


def get_unread_contact_messages():
    """Get unread contact messages."""
    return ContactMessage.query.filter_by(is_read=False).order_by(ContactMessage.created_at.desc()).all()


def get_contact_message_by_id(msg_id):
    """Get contact message by ID."""
    return ContactMessage.query.get(msg_id)


def mark_contact_message_read(msg_id):
    """Mark contact message as read."""
    msg = ContactMessage.query.get(msg_id)
    if msg:
        msg.is_read = True
        db.session.commit()
        return True
    return False


def reply_to_contact_message(msg_id, reply):
    """Add reply to contact message."""
    msg = ContactMessage.query.get(msg_id)
    if msg:
        msg.admin_reply = reply
        msg.is_read = True
        db.session.commit()
        return True
    return False


def delete_contact_message(msg_id):
    """Delete contact message."""
    msg = ContactMessage.query.get(msg_id)
    if msg:
        db.session.delete(msg)
        db.session.commit()
        return True
    return False


def get_unread_contact_count():
    """Get count of unread messages."""
    return ContactMessage.query.filter_by(is_read=False).count()

def get_admins_count():
    """Get total admin count."""
    return Admin.query.count()


# ==================== Settings Functions ====================

def get_setting(key):
    """Get setting value by key."""
    setting = Setting.query.filter_by(key=key).first()
    return setting.value if setting else None


def update_setting(key, value):
    """Update setting value."""
    setting = Setting.query.filter_by(key=key).first()
    if setting:
        setting.value = value
        db.session.commit()


def get_all_settings():
    """Get all settings as dictionary."""
    settings = Setting.query.all()
    return {s.key: s.value for s in settings}


def get_shop_timings():
    """Get shop opening and closing times."""
    settings = get_all_settings()
    return {
        'open_time': settings.get('shop_open_time', '08:00'),
        'close_time': settings.get('shop_close_time', '21:00'),
        'phone': settings.get('shop_phone', '9999999999')
    }
