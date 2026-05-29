import math
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from functools import wraps
from database.models import Subject, AttendanceSession, AttendanceRecord, db
from sqlalchemy import func

student_bp = Blueprint('student', __name__)

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula
    R = 6371000 # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@student_bp.route('/dashboard')
@student_required
def dashboard():
    # Calculate overall attendance
    total_sessions_query = db.session.query(AttendanceSession.id).all()
    total_sessions = len(total_sessions_query)
    
    attended_sessions_query = AttendanceRecord.query.filter_by(student_id=current_user.id).all()
    attended_sessions = len(attended_sessions_query)
    
    overall_percentage = (attended_sessions / total_sessions * 100) if total_sessions > 0 else 0
    
    # Calculate subject-wise attendance
    subjects = Subject.query.all()
    subject_attendance = []
    
    for subject in subjects:
        total_sub_sessions = AttendanceSession.query.filter_by(subject_id=subject.id).count()
        if total_sub_sessions > 0:
            attended_sub_sessions = db.session.query(AttendanceRecord).join(AttendanceSession).filter(
                AttendanceSession.subject_id == subject.id,
                AttendanceRecord.student_id == current_user.id
            ).count()
            percentage = (attended_sub_sessions / total_sub_sessions * 100)
            subject_attendance.append({
                'subject_name': subject.name,
                'total': total_sub_sessions,
                'attended': attended_sub_sessions,
                'percentage': round(percentage, 2)
            })
            
    recent_records = AttendanceRecord.query.filter_by(student_id=current_user.id).order_by(AttendanceRecord.timestamp.desc()).limit(10).all()
            
    return render_template('student/dashboard.html', 
                           overall_percentage=round(overall_percentage, 2),
                           total_sessions=total_sessions,
                           attended_sessions=attended_sessions,
                           subject_attendance=subject_attendance,
                           recent_records=recent_records)

@student_bp.route('/scan')
@student_required
def scan():
    return render_template('student/scanner.html')

@student_bp.route('/mark/<token>')
@student_required
def mark_attendance(token):
    session = AttendanceSession.query.filter_by(token=token, is_active=True).first()
    if not session:
        flash('Invalid or expired QR code.', 'danger')
        return redirect(url_for('student.dashboard'))
        
    return render_template('student/verify_location.html', token=token, session=session)

@student_bp.route('/api/mark_with_location', methods=['POST'])
@student_required
def mark_with_location():
    data = request.json
    token = data.get('token')
    lat = data.get('latitude')
    lon = data.get('longitude')
    
    if not token or lat is None or lon is None:
        return {'success': False, 'message': 'Missing location data.'}, 400
        
    session = AttendanceSession.query.filter_by(token=token, is_active=True).first()
    if not session:
        return {'success': False, 'message': 'Invalid or ended session.'}, 400
        
    # Check if expired
    expiry_time = session.created_at + timedelta(minutes=current_app.config['SESSION_EXPIRY_MINUTES'])
    if datetime.utcnow() > expiry_time:
        # Auto-close session
        session.is_active = False
        db.session.commit()
        return {'success': False, 'message': 'This QR code has expired (time limit exceeded).'}, 400

    # Check Distance
    if session.latitude is None or session.longitude is None:
        return {'success': False, 'message': 'The faculty did not provide a location for this session.'}, 400
        
    campus_lat = session.latitude
    campus_lon = session.longitude
    allowed_radius = current_app.config['ALLOWED_RADIUS_METERS']
    
    distance = calculate_distance(float(lat), float(lon), campus_lat, campus_lon)
    
    if distance > allowed_radius:
        return {'success': False, 'message': f'You are too far from the classroom ({round(distance)}m). Allowed radius is {allowed_radius}m.'}, 403

    # Check if already marked
    existing_record = AttendanceRecord.query.filter_by(session_id=session.id, student_id=current_user.id).first()
    if existing_record:
        return {'success': False, 'message': 'Attendance already marked for this session.'}, 400
        
    new_record = AttendanceRecord(session_id=session.id, student_id=current_user.id)
    db.session.add(new_record)
    db.session.commit()
    
    return {'success': True, 'message': f'Attendance successfully marked for {session.subject.name}!'}
