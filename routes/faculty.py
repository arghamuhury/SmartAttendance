import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from database.models import Subject, AttendanceSession, AttendanceRecord, db
from datetime import date

faculty_bp = Blueprint('faculty', __name__)

def faculty_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'faculty':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@faculty_bp.route('/dashboard')
@faculty_required
def dashboard():
    subjects = Subject.query.all()
    active_sessions = AttendanceSession.query.filter_by(faculty_id=current_user.id, is_active=True).all()
    past_sessions = AttendanceSession.query.filter_by(faculty_id=current_user.id, is_active=False).order_by(AttendanceSession.date.desc()).limit(10).all()
    return render_template('faculty/dashboard.html', subjects=subjects, active_sessions=active_sessions, past_sessions=past_sessions)

@faculty_bp.route('/start_session', methods=['POST'])
@faculty_required
def start_session():
    subject_id = request.form.get('subject_id')
    lat = request.form.get('latitude')
    lon = request.form.get('longitude')
    
    if not subject_id:
        flash('Subject is required.', 'danger')
        return redirect(url_for('faculty.dashboard'))
        
    token = str(uuid.uuid4())
    session = AttendanceSession(
        faculty_id=current_user.id, 
        subject_id=subject_id, 
        token=token, 
        date=date.today(),
        latitude=float(lat) if lat else None,
        longitude=float(lon) if lon else None
    )
    db.session.add(session)
    db.session.commit()
    
    return redirect(url_for('faculty.live_qr', session_id=session.id))

@faculty_bp.route('/live_qr/<int:session_id>')
@faculty_required
def live_qr(session_id):
    session = AttendanceSession.query.get_or_404(session_id)
    if session.faculty_id != current_user.id or not session.is_active:
        flash('Invalid or inactive session.', 'danger')
        return redirect(url_for('faculty.dashboard'))
        
    # Generate the URL that students will hit
    qr_url = url_for('student.mark_attendance', token=session.token, _external=True)
    
    records = AttendanceRecord.query.filter_by(session_id=session.id).all()
    
    return render_template('faculty/live_qr.html', session=session, qr_url=qr_url, records=records)

@faculty_bp.route('/end_session/<int:session_id>', methods=['POST'])
@faculty_required
def end_session(session_id):
    session = AttendanceSession.query.get_or_404(session_id)
    if session.faculty_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('faculty.dashboard'))
        
    session.is_active = False
    db.session.commit()
    flash('Session ended.', 'success')
    return redirect(url_for('faculty.dashboard'))

@faculty_bp.route('/session_records/<int:session_id>')
@faculty_required
def session_records(session_id):
    session = AttendanceSession.query.get_or_404(session_id)
    if session.faculty_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('faculty.dashboard'))
        
    records = AttendanceRecord.query.filter_by(session_id=session.id).all()
    return render_template('faculty/session_records.html', session=session, records=records)
