from flask import Blueprint, render_template
from flask_login import login_required
from database.models import Student, Attendance
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    total_students = Student.query.count()
    
    # Today's attendance stats
    today = datetime.now().date()
    today_attendance = Attendance.query.filter_by(date=today).count()
    
    attendance_percentage = 0
    if total_students > 0:
        attendance_percentage = round((today_attendance / total_students) * 100, 2)
        
    recent_logs = Attendance.query.order_by(Attendance.date.desc(), Attendance.time.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                           total_students=total_students,
                           today_attendance=today_attendance,
                           attendance_percentage=attendance_percentage,
                           recent_logs=recent_logs)
