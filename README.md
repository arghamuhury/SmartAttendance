# Smart Attendance System

Welcome to the **Smart Attendance System**, a modern, comprehensive, and automated web-based solution designed to streamline the attendance tracking process in educational institutions. 

By leveraging dynamic QR code generation coupled with real-time geographical location (geolocation) verification, this system eradicates the inefficiencies and vulnerabilities of traditional roll-call methods, ensuring secure, proxy-free, and rapid attendance logging.

## Overview

Traditional attendance management is often a tedious process that consumes valuable lecture time and is highly prone to human error or proxy attendance. The Smart Attendance System addresses these critical pain points by providing a fully digital, highly secure, and role-based environment. 

The system operates on a seamless workflow: 
1. **Faculty Initiation:** A faculty member initiates an attendance session for a specific class or subject from their dashboard.
2. **QR Code Generation:** The system instantly generates a unique, time-sensitive QR code displayed on the projector or faculty's screen.
3. **Student Scanning & Verification:** Students scan this QR code using their smartphones. Upon scanning, the system requests the student's current GPS location and calculates the spatial distance between the student and the faculty.
4. **Attendance Marking:** If the student is physically within the classroom's permissible radius, their attendance is successfully logged in the database.

## Key Features

- **Role-Based Access Control (RBAC)**: Secure, customized portals tailored specifically for Administrators, Faculty members, and Students.
- **Admin Dashboard**: A powerful administrative interface to manage system users (add/edit/delete students and faculty), manage academic subjects, and view system-wide attendance reports and analytics.
- **Faculty Portal**: Allows faculty to generate live QR codes for their classes, track historical session records, monitor individual student attendance, and export attendance sheets.
- **Student Portal**: Enables students to securely scan session QR codes, verify their location, and access personal attendance metrics and history to track their academic standing.
- **Geolocation Security**: Intelligent spatial matching algorithms to ensure students are physically present in the classroom, effectively eliminating remote proxy attendance.
- **Responsive Design**: A fully responsive frontend crafted with modern web technologies, ensuring a flawless experience across desktops, tablets, and mobile devices.

## Tech Stack

This project is built using a robust and scalable technology stack:
- **Backend**: Python 3, Flask, Flask-SQLAlchemy (ORM), Flask-Login (Authentication), Flask-Bcrypt (Password Hashing)
- **Database**: MySQL / SQLite (configured dynamically via SQLAlchemy)
- **Frontend**: HTML5, Vanilla CSS3, JavaScript, Jinja2 Templating Engine
- **Deployment & Hosting**: PythonAnywhere (Production Environment)

## Installation and Setup

Follow these detailed steps to run the Smart Attendance System on your local machine for development and testing purposes.

### 1. Clone the Repository
First, clone the repository to your local machine using Git:
```bash
git clone https://github.com/arghamuhury/SmartAttendance.git
cd SmartAttendance
```

### 2. Create a Virtual Environment
It is highly recommended to isolate your project dependencies using a virtual environment.
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required Python packages listed in the requirements file:
```bash
pip install -r requirements.txt
```

### 4. Environment Variables Configuration
For enhanced security and flexibility, configure your environment variables. Create a `.env` file in the root directory (if utilized by `config.py`) or modify the configuration file to set your database URI and secret keys.

### 5. Run the Application
Start the Flask development server. Upon the first execution, the system will automatically initialize the database schema and seed a default administrative user.
```bash
python app.py
```
*Note: The default administrator credentials seeded are:*
- **Username**: `admin`
- **Password**: `admin123`

## Usage Guide
- Open your preferred web browser and navigate to the production environment: `https://smartattendance.pythonanywhere.com/` (or `http://127.0.0.1:5000` if running locally).
- **Admins:** Log in using the admin credentials to set up faculty accounts, student accounts, and subjects.
- **Faculty:** Log in to start a new attendance session and project the generated QR code to the class.
- **Students:** Log in to the student portal on a mobile device and use the built-in scanner to scan the faculty's QR code and mark presence.

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software as per the terms of the license.
