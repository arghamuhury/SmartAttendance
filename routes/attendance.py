from flask import Blueprint, render_template, request, Response
from flask_login import login_required
from database.models import Attendance, Student
import csv
from io import StringIO
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/attendance')
@login_required
def index():
    date_filter = request.args.get('date')
    
    query = Attendance.query.join(Student).order_by(Attendance.date.desc(), Attendance.time.desc())
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(Attendance.date == filter_date)
        except ValueError:
            pass
            
    attendances = query.all()
    return render_template('attendance.html', attendances=attendances, date_filter=date_filter)

@attendance_bp.route('/attendance/export')
@login_required
def export_csv():
    attendances = Attendance.query.join(Student).order_by(Attendance.date.desc(), Attendance.time.desc()).all()
    
    def generate():
        data = StringIO()
        writer = csv.writer(data)
        
        # Write header
        writer.writerow(['Student ID', 'Name', 'Department', 'Semester', 'Date', 'Time', 'Status'])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        
        # Write rows
        for record in attendances:
            writer.writerow([
                record.student.student_id,
                record.student.name,
                record.student.department,
                record.student.semester,
                record.date.strftime('%Y-%m-%d'),
                record.time.strftime('%H:%M:%S'),
                record.status
            ])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)
            
    response = Response(generate(), mimetype='text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename=f'attendance_export_{datetime.now().strftime("%Y%m%d")}.csv')
    return response

@attendance_bp.route('/reports')
@login_required
def reports():
    # Gather data for charts (e.g. attendance over last 7 days)
    # Simple mockup for the frontend to render with Chart.js
    return render_template('reports.html')
