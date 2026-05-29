import os

class Config:
    # Secret key for session management and flash messages
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-attendance-system'
    
    # Database Configuration (SQLite)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Geolocation Settings
    # Example coordinates (Change these to the actual campus location)
    CAMPUS_LATITUDE = 28.704060
    CAMPUS_LONGITUDE = 77.102493
    ALLOWED_RADIUS_METERS = 100
    SESSION_EXPIRY_MINUTES = 5

    # Uploads and Dataset configurations
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    EXPORTS_DIR = os.path.join(BASE_DIR, 'attendance_exports')
