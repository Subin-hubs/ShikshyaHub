from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.models import Student, Enrollment, Course, Attendance, Grade, Assignment, db
from datetime import datetime
from werkzeug.utils import secure_filename
import os

student = Blueprint('student', __name__)

# Helper to get student info
def get_student_info():
    student_info = Student.query.filter_by(user_id=current_user.id).first()
    if not student_info:
        flash('Student profile not found.', 'warning')
        return None
    return student_info

@student.route('/student/dashboard')
@login_required
def dashboard():
    # Only let students access this page
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    student_info = get_student_info()
    if student_info is None:
        return render_template('student/dashboard.html', student=None, enrollments=[])
    
    enrollments = Enrollment.query.filter_by(student_id=student_info.id).all()
    return render_template('student/dashboard.html', student=student_info, enrollments=enrollments)

@student.route('/student/courses')
@login_required
def courses():
    student_info = get_student_info()
    if not student_info:
        return redirect(url_for('student.dashboard'))
    enrollments = Enrollment.query.filter_by(student_id=student_info.id).all()
    return render_template('student/courses.html', enrollments=enrollments)

@student.route('/student/attendance')
@login_required
def attendance():
    student_info = get_student_info()
    if not student_info:
        return redirect(url_for('student.dashboard'))
    attendance_records = Attendance.query.filter_by(student_id=student_info.id).all()
    return render_template('student/attendance.html', attendance=attendance_records)

@student.route('/student/grades')
@login_required
def grades():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    student_info = get_student_info()
    if not student_info:
        return redirect(url_for('student.dashboard'))
    
    grades_data = Grade.query.filter_by(student_id=student_info.id).all()
    
    # Calculate GPA (if marks are available)
    total_marks = 0
    total_courses = 0
    for grade in grades_data:
        if grade.marks and grade.total:
            percentage = (grade.marks / grade.total) * 100
            total_marks += percentage
            total_courses += 1
    
    gpa = round(total_marks / total_courses, 2) if total_courses > 0 else 0
    
    return render_template('student/grades.html', grades=grades_data, gpa=gpa, total_courses=total_courses)

@student.route('/student/notices')
@login_required
def notices():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    # Placeholder - implement based on your Notice model
    notices_data = []
    return render_template('student/notices.html', notices=notices_data)

@student.route('/student/assignments')
@login_required
def assignments():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    student_info = get_student_info()
    if not student_info:
        return redirect(url_for('student.dashboard'))
    
    # Get all assignments from enrolled courses
    enrollments = Enrollment.query.filter_by(student_id=student_info.id).all()
    course_ids = [e.course_id for e in enrollments]
    assignments_data = Assignment.query.filter(Assignment.course_id.in_(course_ids)).all()
    
    return render_template('student/assignments.html', assignments=assignments_data)

# ==================== STUDENT API ENDPOINTS ====================

@student.route('/student/api/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll_course(course_id):
    """Enroll student in a course"""
    if current_user.role != 'student':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    student_info = get_student_info()
    if not student_info:
        return jsonify({'success': False, 'message': 'Student profile not found'}), 404
    
    # Check if already enrolled
    existing = Enrollment.query.filter_by(
        student_id=student_info.id, 
        course_id=course_id
    ).first()
    
    if existing:
        return jsonify({'success': False, 'message': 'Already enrolled in this course'}), 400
    
    try:
        enrollment = Enrollment(student_id=student_info.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        flash('Successfully enrolled in course!', 'success')
        return jsonify({'success': True, 'message': 'Enrolled successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@student.route('/student/api/unenroll/<int:course_id>', methods=['POST'])
@login_required
def unenroll_course(course_id):
    """Unenroll student from a course"""
    if current_user.role != 'student':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    student_info = get_student_info()
    if not student_info:
        return jsonify({'success': False, 'message': 'Student profile not found'}), 404
    
    try:
        enrollment = Enrollment.query.filter_by(
            student_id=student_info.id,
            course_id=course_id
        ).first()
        
        if not enrollment:
            return jsonify({'success': False, 'message': 'Not enrolled in this course'}), 404
        
        db.session.delete(enrollment)
        db.session.commit()
        flash('Successfully unenrolled from course!', 'success')
        return jsonify({'success': True, 'message': 'Unenrolled successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@student.route('/student/api/submit-assignment/<int:assignment_id>', methods=['POST'])
@login_required
def submit_assignment(assignment_id):
    """Submit assignment"""
    if current_user.role != 'student':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    student_info = get_student_info()
    if not student_info:
        return jsonify({'success': False, 'message': 'Student profile not found'}), 404
    
    try:
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify({'success': False, 'message': 'Assignment not found'}), 404
        
        # Handle file upload if provided
        if 'file' in request.files:
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                upload_path = os.path.join('app/static/uploads/assignments', f'{assignment_id}_{student_info.id}_{filename}')
                file.save(upload_path)
                flash('Assignment submitted successfully!', 'success')
                return jsonify({'success': True, 'message': 'Submitted successfully'})
        
        flash('Please select a file to upload', 'warning')
        return jsonify({'success': False, 'message': 'No file provided'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500