"""
Shivkumar Kirana Store - Main Flask Application
A complete grocery shop management system with customer website, chatbot, and admin panel.
PostgreSQL + Flask-SQLAlchemy + Flask-Migrate
"""

import os
import json
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

from config import Config
from models import (
    db, init_db, get_all_products, get_product_by_id, search_products,
    add_product, update_product, delete_product, get_products_count,
    create_order, get_all_orders, get_orders_count, delete_order, update_order_status,
    get_admin_by_username, get_all_admins, add_admin, delete_admin, get_admins_count,
    is_master_admin, get_admin_by_id, toggle_product_availability, get_available_products,
    get_unavailable_count, get_shop_timings, update_setting, get_all_settings,
    get_orders_by_mobile, add_customer_care_issue, get_all_customer_care_issues,
    get_customer_care_issue_by_id, get_customer_care_issues_by_status,
    update_customer_care_issue, delete_customer_care_issue, get_open_customer_care_count,
    add_contact_message, get_all_contact_messages, get_contact_message_by_id,
    mark_contact_message_read, reply_to_contact_message, delete_contact_message,
    get_unread_contact_count
)


app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy and Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Create tables at startup (for production on Render)
with app.app_context():
    db.create_all()
    # Create default settings if not exist
    from models import _create_default_settings, get_admin_by_username, add_admin
    _create_default_settings()
    
    # Create default admin if not exists
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD')
    if admin_password and not get_admin_by_username(admin_username):
        password_hash = generate_password_hash(admin_password)
        add_admin(admin_username, password_hash, is_master=True)
        print(f"Master admin created: {admin_username}")

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def admin_required(f):
    """Decorator to require admin login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('कृपया पहले लॉगिन करें (Please login first)', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function
# ==================== about Routes ====================

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form submission
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            message = request.form.get('message', '').strip()
            
            if not all([name, email, message]):
                flash('कृपया सभी फील्ड भरें (Please fill all fields)', 'error')
                return redirect(url_for('contact'))
            
            # Store contact message in database
            msg_id = add_contact_message(name, email, message)
            if msg_id:
                flash(f'आपका संदेश प्राप्त हो गया! आप अपना जवाब यहाँ देख सकते हैं: {url_for("check_reply", _external=True)}', 'success')
            else:
                flash('संदेश भेजने में त्रुटि हुई (Error sending message)', 'error')
            return redirect(url_for('contact'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('contact'))
    
    return render_template("contact.html")


@app.route("/check-reply", methods=['GET', 'POST'])
def check_reply():
    """Customer can check their message replies."""
    messages = []
    email = None
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if email:
            # Search for all messages from this email
            all_msgs = get_all_contact_messages()
            messages = [msg for msg in all_msgs if msg.email.lower() == email.lower()]
            if not messages:
                messages = []
    
    return render_template("check_reply.html", messages=messages, email=email)


@app.route("/customer-care")
def customer_care():
    """Customer Care page."""
    return render_template("customer_care/index.html")


@app.route('/api/customer-care/report', methods=['POST'])
def report_customer_care_issue():
    """API endpoint to report a customer care issue."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'issue_type', 'description']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Add issue to database
        issue_id = add_customer_care_issue(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            issue_type=data.get('issue_type'),
            description=data.get('description'),
            order_id=data.get('order_id', None),
            priority=data.get('priority', 'normal')
        )
        
        if issue_id:
            return jsonify({
                'success': True,
                'message': 'आपकी समस्या दर्ज की जा गई है। हम 24 घंटे में आपसे संपर्क करेंगे। (Your issue has been reported. We will contact you within 24 hours.)',
                'issue_id': issue_id
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Failed to submit issue'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== Customer Routes ====================

@app.route('/')
def index():
    """Home page with featured products (only available ones)."""
    products = get_available_products()
    shop_timings = get_shop_timings()
    return render_template('index.html', products=products[:8], shop=shop_timings)

@app.route('/products')
def products():
    """All products page."""
    search_query = request.args.get('search', '')
    if search_query:
        products_list = search_products(search_query)
    else:
        products_list = get_all_products()
    return render_template('products.html', products=products_list, search_query=search_query)

@app.route('/checkout')
def checkout():
    """Checkout page."""
    return render_template('checkout.html')

@app.route('/my-orders')
def my_orders():
    """My Orders page - customers can view their orders."""
    return render_template('my_orders.html')

@app.route('/api/my-orders/<mobile>')
def get_customer_orders(mobile):
    """API endpoint to get orders by mobile number."""
    try:
        orders = get_orders_by_mobile(mobile)
        orders_list = []
        for order in orders:
            orders_list.append({
                'id': order.id,
                'customer_name': order.customer_name,
                'mobile': order.mobile,
                'address': order.address,
                'items': order.items,
                'total': order.total,
                'status': order.status,
                'created_at': order.date.isoformat() if order.date else None
            })
        return jsonify({'success': True, 'orders': orders_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/place-order', methods=['POST'])
def place_order():
    """API endpoint to place an order."""
    try:
        data = request.get_json()
        
        customer_name = data.get('customer_name', '').strip()
        mobile = data.get('mobile', '').strip()
        address = data.get('address', '').strip()
        items = data.get('items', [])
        total = data.get('total', 0)
        payment_method = data.get('payment_method', 'cod')
        
        if not customer_name or not mobile or not address or not items:
            return jsonify({'success': False, 'message': 'सभी फील्ड भरें (Please fill all fields)'}), 400
        
        # Save order to database with payment method
        order_id = create_order(customer_name, mobile, address, items, total, payment_method)
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'payment_method': payment_method,
            'total': total
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Chatbot API endpoint."""
    data = request.get_json()
    user_message = data.get('message', '').strip().lower()
    
    if not user_message:
        return jsonify({'reply': 'कृपया कुछ टाइप करें (Please type something)'})
    
    # Greetings
    greetings = ['hi', 'hello', 'नमस्ते', 'हेलो', 'हाय']
    if any(greet in user_message for greet in greetings):
        return jsonify({'reply': 'नमस्ते! 🙏 Shivkumar Kirana Store में आपका स्वागत है। आप किस सामान का दाम जानना चाहते हैं?'})
    
    # Help
    if 'help' in user_message or 'मदद' in user_message:
        return jsonify({'reply': 'आप किसी भी सामान का नाम टाइप करें, मैं उसका दाम बताऊंगा। जैसे: "चावल", "आटा", "तेल" आदि।'})
    
    # Search for product
    products = search_products(user_message)
    
    if products:
        if len(products) == 1:
            p = products[0]
            return jsonify({
                'reply': f"✅ *{p.name}*\n💰 कीमत: ₹{p.price}\n📦 उपलब्ध है (Available)"
            })
        else:
            reply = f"मिलते-जुलते {len(products)} सामान मिले:\n\n"
            for p in products[:5]:
                reply += f"• {p.name} - ₹{p.price}\n"
            return jsonify({'reply': reply})
    else:
        return jsonify({
            'reply': f"❌ '{user_message}' उपलब्ध नहीं है (Not available)\n\nकृपया अन्य सामान खोजें या दुकान पर संपर्क करें।"
        })

# ==================== Admin Routes ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        admin = get_admin_by_username(username)
        
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash('सफलतापूर्वक लॉगिन (Login successful)!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('गलत यूजरनेम या पासवर्ड (Invalid credentials)', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout."""
    session.clear()
    flash('लॉगआउट सफल (Logout successful)', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard."""
    stats = {
        'products': get_products_count(),
        'orders': get_orders_count(),
        'admins': get_admins_count()
    }
    recent_orders = get_all_orders()[:5]
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)

@app.route('/admin/products')
@admin_required
def admin_products():
    """Admin product management."""
    products_list = get_all_products()
    return render_template('admin/products.html', products=products_list)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Add new product."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price = request.form.get('price', 0)
        
        try:
            price = float(price)
        except ValueError:
            flash('कृपया सही कीमत दर्ज करें (Enter valid price)', 'error')
            return redirect(url_for('admin_add_product'))
        
        # Handle image upload
        image_filename = 'default.png'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid conflicts
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        add_product(name, price, image_filename)
        flash(f'"{name}" सफलतापूर्वक जोड़ा गया (Product added)', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/add_product.html')

@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    """Edit product."""
    product = get_product_by_id(product_id)
    if not product:
        flash('प्रोडक्ट नहीं मिला (Product not found)', 'error')
        return redirect(url_for('admin_products'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price = request.form.get('price', 0)
        
        try:
            price = float(price)
        except ValueError:
            flash('कृपया सही कीमत दर्ज करें (Enter valid price)', 'error')
            return redirect(url_for('admin_edit_product', product_id=product_id))
        
        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        update_product(product_id, name, price, image_filename)
        flash(f'"{name}" अपडेट हो गया (Product updated)', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/edit_product.html', product=product)

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    """Delete product."""
    product = get_product_by_id(product_id)
    if product:
        delete_product(product_id)
        flash('प्रोडक्ट डिलीट हो गया (Product deleted)', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    """Admin order management."""
    orders_list = get_all_orders()
    # Parse JSON items for display
    orders_parsed = []
    for order in orders_list:
        order_dict = {
            'id': order.id,
            'customer_name': order.customer_name,
            'mobile': order.mobile,
            'address': order.address,
            'items': order.items,
            'total': order.total,
            'payment_method': order.payment_method,
            'status': order.status,
            'date': order.date
        }
        order_dict['items_list'] = json.loads(order.items)
        orders_parsed.append(order_dict)
    return render_template('admin/orders.html', orders=orders_parsed)

@app.route('/admin/orders/delete/<int:order_id>', methods=['POST'])
@admin_required
def admin_delete_order(order_id):
    """Delete order."""
    delete_order(order_id)
    flash('ऑर्डर डिलीट हो गया (Order deleted)', 'success')
    return redirect(url_for('admin_orders'))

@app.route('/admin/orders/status/<int:order_id>', methods=['POST'])
@admin_required
def admin_update_order_status(order_id):
    """Update order status."""
    status = request.form.get('status', 'pending')
    valid_statuses = ['pending', 'confirmed', 'delivered', 'cancelled']
    if status in valid_statuses:
        update_order_status(order_id, status)
        status_names = {'pending': 'Pending', 'confirmed': 'Confirmed', 'delivered': 'Delivered', 'cancelled': 'Cancelled'}
        flash(f'Order #{order_id} status updated to {status_names[status]}', 'success')
    return redirect(url_for('admin_orders'))


@app.route('/admin/availability')
@admin_required
def admin_availability():
    """Product availability management."""
    products_list = get_all_products()
    unavailable_count = get_unavailable_count()
    return render_template('admin/availability.html', products=products_list, unavailable_count=unavailable_count)

@app.route('/admin/availability/toggle/<int:product_id>', methods=['POST'])
@admin_required
def admin_toggle_availability(product_id):
    """Toggle product availability."""
    product = get_product_by_id(product_id)
    if product:
        new_status = toggle_product_availability(product_id)
        status_text = "उपलब्ध (Available)" if new_status else "उपलब्ध नहीं (Unavailable)"
        flash(f'"{product.name}" अब {status_text}', 'success')
    return redirect(url_for('admin_availability'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    """Shop settings management."""
    if request.method == 'POST':
        open_time = request.form.get('open_time', '08:00')
        close_time = request.form.get('close_time', '21:00')
        phone = request.form.get('phone', '')
        
        update_setting('shop_open_time', open_time)
        update_setting('shop_close_time', close_time)
        update_setting('shop_phone', phone)
        
        flash('सेटिंग्स अपडेट हो गई (Settings updated)', 'success')
        return redirect(url_for('admin_settings'))
    
    settings = get_all_settings()
    return render_template('admin/settings.html', settings=settings)

@app.route('/admin/admins')
@admin_required
def admin_admins():
    """Admin user management."""
    admins_list = get_all_admins()
    current_is_master = is_master_admin(session.get('admin_id'))
    return render_template('admin/admins.html', admins=admins_list, current_is_master=current_is_master)

@app.route('/admin/admins/add', methods=['POST'])
@admin_required
def admin_add_admin():
    """Add new admin - only master can add."""
    # Only master admin can add new admins
    if not is_master_admin(session.get('admin_id')):
        flash('केवल Master Admin नए एडमिन जोड़ सकते हैं (Only Master Admin can add new admins)', 'error')
        return redirect(url_for('admin_admins'))
    
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        flash('यूजरनेम और पासवर्ड दोनों जरूरी हैं', 'error')
        return redirect(url_for('admin_admins'))
    
    if len(password) < 6:
        flash('पासवर्ड कम से कम 6 अक्षर का होना चाहिए', 'error')
        return redirect(url_for('admin_admins'))
    
    password_hash = generate_password_hash(password)
    result = add_admin(username, password_hash)  # is_master defaults to False
    
    if result:
        flash(f'नया एडमिन "{username}" जोड़ा गया', 'success')
    else:
        flash('यह यूजरनेम पहले से मौजूद है', 'error')
    
    return redirect(url_for('admin_admins'))

@app.route('/admin/admins/delete/<int:admin_id>', methods=['POST'])
@admin_required
def admin_delete_admin(admin_id):
    """Delete admin - only master can delete, master cannot be deleted."""
    # Only master admin can delete other admins
    if not is_master_admin(session.get('admin_id')):
        flash('केवल Master Admin एडमिन डिलीट कर सकते हैं (Only Master Admin can delete admins)', 'error')
        return redirect(url_for('admin_admins'))
    
    if admin_id == session.get('admin_id'):
        flash('आप खुद को डिलीट नहीं कर सकते', 'error')
    else:
        result = delete_admin(admin_id)
        if result:
            flash('एडमिन डिलीट हो गया', 'success')
        else:
            flash('Master Admin को डिलीट नहीं किया जा सकता (Cannot delete Master Admin)', 'error')
    return redirect(url_for('admin_admins'))

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ==================== Initialize & Run ====================

def setup_default_admin():
    """Setup default admin if not exists."""
    from models import get_admin_by_username, add_admin
    
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD')
    
    if admin_password and not get_admin_by_username(admin_username):
        password_hash = generate_password_hash(admin_password)
        add_admin(admin_username, password_hash, is_master=True)
        print(f"Master admin created: {admin_username}")

def setup_sample_products():
    """Add sample products if database is empty."""
    from models import get_products_count, add_product
    
    if get_products_count() == 0:
        sample_products = [
            ('चावल (Rice) - 1kg', 60),
            ('गेहूं आटा (Wheat Flour) - 1kg', 45),
            ('चीनी (Sugar) - 1kg', 50),
            ('नमक (Salt) - 1kg', 25),
            ('सरसों तेल (Mustard Oil) - 1L', 180),
            ('दाल (Toor Dal) - 1kg', 140),
            ('चाय पत्ती (Tea) - 250g', 80),
            ('हल्दी (Turmeric) - 100g', 35),
            ('मिर्च पाउडर (Chili Powder) - 100g', 40),
            ('धनिया पाउडर (Coriander) - 100g', 30),
            ('साबुन (Soap)', 35),
            ('शैम्पू (Shampoo)', 120),
        ]
        
        for name, price in sample_products:
            add_product(name, price)
        
        print(f"Added {len(sample_products)} sample products")


# ==================== Admin Customer Care Routes ====================

@app.route('/admin/customer-care')
@admin_required
def admin_customer_care():
    """Admin customer care issues dashboard."""
    issues = get_all_customer_care_issues()
    open_count = get_open_customer_care_count()
    return render_template('admin/customer_care.html', issues=issues, open_count=open_count)


@app.route('/admin/customer-care/<int:issue_id>')
@admin_required
def admin_view_customer_care_issue(issue_id):
    """View individual customer care issue."""
    issue = get_customer_care_issue_by_id(issue_id)
    if not issue:
        flash('Issue not found', 'error')
        return redirect(url_for('admin_customer_care'))
    return render_template('admin/customer_care_detail.html', issue=issue)


@app.route('/api/admin/customer-care/<int:issue_id>/respond', methods=['POST'])
@admin_required
def admin_respond_to_issue(issue_id):
    """Admin responds to customer care issue."""
    try:
        data = request.get_json()
        response = data.get('response', '').strip()
        status = data.get('status', 'open')
        
        if not response:
            return jsonify({'success': False, 'message': 'Response cannot be empty'}), 400
        
        resolved_at = datetime.utcnow() if status == 'resolved' else None
        
        if update_customer_care_issue(issue_id, status=status, admin_response=response, resolved_at=resolved_at):
            return jsonify({'success': True, 'message': 'Response sent successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to update issue'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/admin/customer-care/<int:issue_id>/delete', methods=['POST'])
@admin_required
def admin_delete_customer_care_issue(issue_id):
    """Admin deletes customer care issue."""
    try:
        if delete_customer_care_issue(issue_id):
            return jsonify({'success': True, 'message': 'Issue deleted successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to delete issue'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== Admin Contact Messages Routes ====================

@app.route('/admin/messages')
@admin_required
def admin_contact_messages():
    """Admin contact messages dashboard."""
    messages = get_all_contact_messages()
    unread_count = get_unread_contact_count()
    return render_template('admin/contact_messages.html', messages=messages, unread_count=unread_count)


@app.route('/admin/messages/<int:msg_id>')
@admin_required
def admin_view_contact_message(msg_id):
    """View individual contact message."""
    message = get_contact_message_by_id(msg_id)
    if not message:
        flash('Message not found', 'error')
        return redirect(url_for('admin_contact_messages'))
    mark_contact_message_read(msg_id)
    return render_template('admin/contact_message_detail.html', message=message)


@app.route('/api/admin/messages/<int:msg_id>/reply', methods=['POST'])
@admin_required
def admin_reply_to_message(msg_id):
    """Admin replies to contact message."""
    try:
        data = request.get_json()
        reply = data.get('reply', '').strip()
        
        if not reply:
            return jsonify({'success': False, 'message': 'Reply cannot be empty'}), 400
        
        if reply_to_contact_message(msg_id, reply):
            return jsonify({'success': True, 'message': 'Reply sent successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to send reply'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/admin/messages/<int:msg_id>/delete', methods=['POST'])
@admin_required
def admin_delete_contact_message(msg_id):
    """Admin deletes contact message."""
    try:
        if delete_contact_message(msg_id):
            return jsonify({'success': True, 'message': 'Message deleted successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to delete message'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        # Create tables (in case migrations haven't run)
        db.create_all()
        
        # Setup default data
        from models import _create_default_settings
        _create_default_settings()
        setup_default_admin()
        setup_sample_products()
    
    print("\n" + "="*50)
    print("  Shivkumar Kirana Store")
    print("="*50)
    print(f"  Website: http://localhost:5000")
    print(f"  Admin Panel: http://localhost:5000/admin")
    print(f"  Admin Login: Use credentials from .env file")
    print("="*50 + "\n")
    
    app.run( host='0.0.0.0', port=5000)
