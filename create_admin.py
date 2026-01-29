#!/usr/bin/env python
from app import app, db
from models import add_admin
from werkzeug.security import generate_password_hash

with app.app_context():
    # Check if admin already exists
    from models import get_admin_by_username
    existing_admin = get_admin_by_username('admin')
    
    if existing_admin:
        print('⚠️  Admin account already exists with username: admin')
    else:
        password_hash = generate_password_hash('admin123')
        admin_id = add_admin('admin', password_hash, is_master=True)
        if admin_id:
            print(f'✅ Admin account created successfully!')
            print(f'   Username: admin')
            print(f'   Password: admin123')
        else:
            print('❌ Error creating admin account')
