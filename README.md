# Smart Attendance System

A comprehensive Smart Attendance System built with Flask, featuring portals for Admins, Faculty, and Students. The system utilizes face recognition and QR codes for seamless and automated attendance tracking.

## Features

- **Admin Portal**: Manage users, subjects, and view overall reports.
- **Faculty Portal**: Generate live QR codes for attendance, track session records, and monitor student attendance.
- **Student Portal**: Scan QR codes, capture face data, verify location, and view personal attendance records.
- **Face Recognition**: Intelligent face matching for authenticating students.
- **Role-based Access**: Secure login system for different types of users (Admin, Faculty, Student) powered by Flask-Login and Flask-Bcrypt.

## Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt
- **Database**: MySQL / SQLite (configured via SQLAlchemy)
- **Frontend**: HTML5, CSS3, JavaScript, Jinja2 Templates

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/arghamuhury/SmartAttendance.git
   cd SmartAttendance
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory (if needed by `config.py`) or configure your database URI appropriately.

5. **Run the Application:**
   ```bash
   python app.py
   ```
   
   *Upon the first run, the database tables will be created automatically, and a default admin user will be seeded.*
   - **Username**: `admin`
   - **Password**: `admin123`

## Usage
- Open your browser and navigate to `https://smartattendance.pythonanywhere.com/`
- Log in using the default admin credentials or as a faculty/student if registered.

## License
MIT License
