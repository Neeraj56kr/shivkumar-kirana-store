"""
Data Migration Script: SQLite to PostgreSQL
Run this AFTER setting up PostgreSQL and running flask db upgrade
"""

import os
import sys
import sqlite3
import json

# Add the app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app import app, db
from models import Product, Order, Admin, Setting

def migrate_data():
    """Migrate data from SQLite to PostgreSQL."""
    sqlite_db = 'kirana.db'
    
    if not os.path.exists(sqlite_db):
        print(f"SQLite database '{sqlite_db}' not found. No data to migrate.")
        return
    
    # Connect to SQLite
    conn = sqlite3.connect(sqlite_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    with app.app_context():
        print("Starting data migration from SQLite to PostgreSQL...")
        
        # Migrate Products
        try:
            cursor.execute('SELECT * FROM products')
            products = cursor.fetchall()
            migrated_products = 0
            for row in products:
                # Check if product already exists
                existing = Product.query.filter_by(name=row['name']).first()
                if not existing:
                    product = Product(
                        name=row['name'],
                        price=row['price'],
                        image=row['image'] if row['image'] else 'default.png',
                        is_available=bool(row['is_available']) if 'is_available' in row.keys() else True
                    )
                    db.session.add(product)
                    migrated_products += 1
            db.session.commit()
            print(f"✅ Migrated {migrated_products} products")
        except Exception as e:
            print(f"❌ Error migrating products: {e}")
            db.session.rollback()
        
        # Migrate Orders
        try:
            cursor.execute('SELECT * FROM orders')
            orders = cursor.fetchall()
            migrated_orders = 0
            for row in orders:
                # Check if order already exists (by customer + mobile + date)
                order = Order(
                    customer_name=row['customer_name'],
                    mobile=row['mobile'],
                    address=row['address'],
                    items=row['items'],
                    total=row['total'],
                    payment_method=row['payment_method'] if 'payment_method' in row.keys() else 'cod',
                    status=row['status'] if 'status' in row.keys() else 'pending'
                )
                db.session.add(order)
                migrated_orders += 1
            db.session.commit()
            print(f"✅ Migrated {migrated_orders} orders")
        except Exception as e:
            print(f"❌ Error migrating orders: {e}")
            db.session.rollback()
        
        # Migrate Admins
        try:
            cursor.execute('SELECT * FROM admins')
            admins = cursor.fetchall()
            migrated_admins = 0
            for row in admins:
                existing = Admin.query.filter_by(username=row['username']).first()
                if not existing:
                    admin = Admin(
                        username=row['username'],
                        password=row['password'],
                        is_master=bool(row['is_master']) if 'is_master' in row.keys() else False
                    )
                    db.session.add(admin)
                    migrated_admins += 1
            db.session.commit()
            print(f"✅ Migrated {migrated_admins} admins")
        except Exception as e:
            print(f"❌ Error migrating admins: {e}")
            db.session.rollback()
        
        # Migrate Settings
        try:
            cursor.execute('SELECT * FROM settings')
            settings = cursor.fetchall()
            migrated_settings = 0
            for row in settings:
                existing = Setting.query.filter_by(key=row['key']).first()
                if not existing:
                    setting = Setting(
                        key=row['key'],
                        value=row['value']
                    )
                    db.session.add(setting)
                    migrated_settings += 1
            db.session.commit()
            print(f"✅ Migrated {migrated_settings} settings")
        except Exception as e:
            print(f"❌ Error migrating settings: {e}")
            db.session.rollback()
        
        print("\n🎉 Data migration complete!")
    
    conn.close()

if __name__ == '__main__':
    migrate_data()
