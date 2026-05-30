import os
from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
from database.models import db, User

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.faculty import faculty_bp
    from routes.student import student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(faculty_bp, url_prefix='/faculty')
    app.register_blueprint(student_bp, url_prefix='/student')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @app.route('/manifest.json')
    def manifest():
        return send_from_directory('static', 'manifest.json')

    @app.route('/sw.js')
    def service_worker():
        response = send_from_directory('static', 'sw.js')
        response.headers['Cache-Control'] = 'no-cache'
        return response

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        # Seed an admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(username='admin', password_hash=hashed_pw, role='admin', name='Super Admin')
            db.session.add(admin)
            db.session.commit()
            print("Default admin created (admin / admin123)")
    app.run(debug=True, host='0.0.0.0')
