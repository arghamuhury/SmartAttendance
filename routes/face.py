from flask import Blueprint, render_template, request, Response, redirect, url_for, flash, jsonify
from flask_login import login_required
from utils.camera import VideoCamera
from utils.face_utils import train_model, load_model
from database.models import db, Student, Attendance
from config import Config
import os
import cv2
import face_recognition
import numpy as np
from datetime import datetime

face_bp = Blueprint('face', __name__)

camera = None

def get_camera():
    global camera
    if not camera:
        camera = VideoCamera()
    return camera

@face_bp.route('/capture/<student_id>')
@login_required
def capture(student_id):
    student = Student.query.filter_by(student_id=student_id).first_or_404()
    return render_template('capture.html', student=student)

def capture_gen(student_id):
    cam = get_camera()
    count = 0
    student_dir = os.path.join(Config.DATASET_DIR, student_id)
    os.makedirs(student_dir, exist_ok=True)
    
    while True:
        frame = cam.get_raw_frame()
        if frame is None:
            break
            
        # Optional: Add face detection here to only save if a face is present
        # But to keep it simple, we save frames as requested by a button press on frontend
        # For auto-capture, we just yield the frame
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@face_bp.route('/video_feed/<student_id>')
@login_required
def video_feed(student_id):
    return Response(capture_gen(student_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@face_bp.route('/save_capture', methods=['POST'])
@login_required
def save_capture():
    student_id = request.form.get('student_id')
    cam = get_camera()
    frame = cam.get_raw_frame()
    if frame is not None:
        student_dir = os.path.join(Config.DATASET_DIR, student_id)
        count = len(os.listdir(student_dir))
        file_path = os.path.join(student_dir, f"{count}.jpg")
        cv2.imwrite(file_path, frame)
        return jsonify({"status": "success", "message": "Image captured!"})
    return jsonify({"status": "error", "message": "Failed to capture image"}), 400

@face_bp.route('/train', methods=['GET', 'POST'])
@login_required
def train():
    if request.method == 'POST':
        try:
            train_model()
            flash('Model trained successfully with the latest dataset!', 'success')
        except Exception as e:
            flash(f'Error training model: {str(e)}', 'danger')
        return redirect(url_for('face.train'))
        
    # Check if model exists
    model_exists = os.path.exists(os.path.join(Config.MODELS_DIR, "encodings.pickle"))
    return render_template('train.html', model_exists=model_exists)

@face_bp.route('/recognize')
@login_required
def recognize():
    return render_template('recognize.html')

def gen_recognize():
    cam = get_camera()
    data = load_model()
    
    if not data:
        print("Model not found. Please train first.")
        return
        
    known_encodings = data["encodings"]
    known_names = data["names"]
    
    while True:
        frame = cam.get_raw_frame()
        if frame is None:
            break
            
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"
            
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]
                
            face_names.append(name)
            
        # Draw boxes and names
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@face_bp.route('/recognize_feed')
@login_required
def recognize_feed():
    return Response(gen_recognize(), mimetype='multipart/x-mixed-replace; boundary=frame')

@face_bp.route('/mark_attendance', methods=['POST'])
@login_required
def mark_attendance():
    """
    Called via AJAX from recognize.html when a face is detected
    """
    cam = get_camera()
    data = load_model()
    
    if not data:
        return jsonify({"status": "error", "message": "Model not trained."})
        
    frame = cam.get_raw_frame()
    if frame is None:
        return jsonify({"status": "error", "message": "No frame captured."})
        
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    if not face_encodings:
         return jsonify({"status": "info", "message": "No face detected."})
         
    known_encodings = data["encodings"]
    known_names = data["names"]
    
    marked = []
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        if True in matches:
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                student_id = known_names[best_match_index]
                
                # Check student exists
                student = Student.query.filter_by(student_id=student_id).first()
                if student:
                    # Check if already marked today
                    today = datetime.now().date()
                    existing = Attendance.query.filter_by(student_id=student.id, date=today).first()
                    
                    if not existing:
                        now = datetime.now()
                        new_attendance = Attendance(
                            student_id=student.id,
                            date=now.date(),
                            time=now.time(),
                            status='Present'
                        )
                        db.session.add(new_attendance)
                        marked.append(student.name)
                        
    if marked:
        db.session.commit()
        return jsonify({"status": "success", "message": f"Attendance marked for: {', '.join(marked)}"})
    else:
        return jsonify({"status": "info", "message": "Face recognized, but attendance already marked or student unknown."})
