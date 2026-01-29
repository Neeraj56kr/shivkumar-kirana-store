"""
Build script for Render deployment.
Creates all database tables and initializes default data.
"""

import os
import sys

# Set up the Flask app
from app import app, db
from models import _create_default_settings
from werkzeug.security import generate_password_hash

def setup_database():
    """Create all tables and initialize data."""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Tables created successfully!")
        
        # Create default settings
        print("Creating default settings...")
        _create_default_settings()
        
        # Create default admin if not exists
        print("Setting up default admin...")
        from models import get_admin_by_username, add_admin
        
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD')
        
        if admin_password and not get_admin_by_username(admin_username):
            password_hash = generate_password_hash(admin_password)
            add_admin(admin_username, password_hash, is_master=True)
            print(f"Master admin created: {admin_username}")
        else:
            print("Admin already exists or ADMIN_PASSWORD not set")
        
        # Add sample products if empty
        from models import get_products_count, add_product
        
        if get_products_count() == 0:
            print("Adding sample products...")
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
        else:
            print(f"Products already exist: {get_products_count()} products")
        
        print("\n✅ Database setup complete!")

if __name__ == '__main__':
    setup_database()
