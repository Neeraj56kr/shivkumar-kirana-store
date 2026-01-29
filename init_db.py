"""Initialize database with default data."""
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from models import init_db, add_product, add_admin, get_admin_by_username, get_products_count

# Load environment variables from .env file
load_dotenv()

def setup_database():
    """Set up database with initial data."""
    print("Initializing database...")
    init_db()
    
    # Add default admin as MASTER if not exists
    # Read credentials from environment variables
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD')
    
    if not admin_password:
        print("WARNING: ADMIN_PASSWORD not set in .env file! Skipping admin creation.")
    elif not get_admin_by_username(admin_username):
        password_hash = generate_password_hash(admin_password)
        add_admin(admin_username, password_hash, is_master=1)  # Master admin
        print(f"Master admin created: {admin_username} (password from .env)")
    
    # Add sample products if database is empty
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
    
    print("Database setup complete!")

if __name__ == '__main__':
    setup_database()
