from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Student, Enrollment, Course, Attendance, Grade

student = Blueprint('student', __name__)

@student.route('/student/dashboard')
@login_required
def dashboard():
    # Only let students access this page
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    # Get student specific data
    student_info = Student.query.filter_by(user_id=current_user.id).first()
    
    # FIX: If the student profile doesn't exist yet, don't crash!
    if student_info is None:
        return render_template('student/dashboard.html', student=None, enrollments=[])
    
    # If student exists, get their data
    enrollments = Enrollment.query.filter_by(student_id=student_info.id).all()
    return render_template('student/dashboard.html', student=student_info, enrollments=enrollments)

@student.route('/student/courses')
@login_required
def courses():
    student_info = Student.query.filter_by(user_id=current_user.id).first()
    if not student_info:
        flash('Profile not found.', 'warning')
        return redirect(url_for('student.dashboard'))
    enrollments = Enrollment.query.filter_by(student_id=student_info.id).all()
    return render_template('student/courses.html', enrollments=enrollments)

@student.route('/student/attendance')
@login_required
def attendance():
    student_info = Student.query.filter_by(user_id=current_user.id).first()
    if not student_info:
        flash('Profile not found.', 'warning')
        return redirect(url_for('student.dashboard'))
    attendance_records = Attendance.query.filter_by(student_id=student_info.id).all()
    return render_template('student/attendance.html', attendance=attendance_records)