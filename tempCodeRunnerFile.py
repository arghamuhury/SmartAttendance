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

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    return app