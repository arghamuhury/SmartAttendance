import os
import sys

# Add parent directory to path so we can import from app
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app import create_app, db, bcrypt
from database.models import Admin

def init_database():
    app = create_app()
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Check if admin already exists
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            print("Creating default admin user...")
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            new_admin = Admin(username='admin', password_hash=hashed_password)
            db.session.add(new_admin)
            db.session.commit()
            print("Default admin created (username: admin, password: admin123)")
        else:
            print("Admin user already exists.")
            
        print("Database initialization complete!")

if __name__ == '__main__':
    init_database()
