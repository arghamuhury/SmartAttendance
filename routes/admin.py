from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from database.models import User, Subject, db
from app import bcrypt

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    students = User.query.filter_by(role='student').count()
    faculty = User.query.filter_by(role='faculty').count()
    subjects = Subject.query.count()
    return render_template('admin/dashboard.html', students=students, faculty=faculty, subjects=subjects)

@admin_bp.route('/users')
@admin_required
def manage_users():
    users = User.query.filter(User.role != 'admin').all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/add_user', methods=['POST'])
@admin_required
def add_user():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    name = request.form.get('name')
    department = request.form.get('department')
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists.', 'danger')
        return redirect(url_for('admin.manage_users'))
        
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=hashed_password, role=role, name=name, department=department)
    db.session.add(new_user)
    db.session.commit()
    flash(f'User {name} added successfully!', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/subjects')
@admin_required
def manage_subjects():
    subjects = Subject.query.all()
    return render_template('admin/subjects.html', subjects=subjects)

@admin_bp.route('/add_subject', methods=['POST'])
@admin_required
def add_subject():
    name = request.form.get('name')
    code = request.form.get('code')
    
    if Subject.query.filter_by(code=code).first():
        flash('Subject code already exists.', 'danger')
        return redirect(url_for('admin.manage_subjects'))
        
    new_subject = Subject(name=name, code=code)
    db.session.add(new_subject)
    db.session.commit()
    flash('Subject added successfully!', 'success')
    return redirect(url_for('admin.manage_subjects'))
