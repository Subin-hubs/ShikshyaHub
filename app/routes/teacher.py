from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.models import Teacher, Course, Attendance, Student, Enrollment, Assignment, Grade, db, User
from datetime import datetime, date
from werkzeug.utils import secure_filename
import os

teacher = Blueprint('teacher', __name__)

# Helper to get teacher info
def get_teacher_info():
    teacher_info = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher_info:
        flash('Teacher profile not found.', 'warning')
        return None
    return teacher_info

@teacher.route('/teacher/dashboard')
@login_required
def dashboard():
    # Only let teachers access this page
    if current_user.role != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    teacher_info = get_teacher_info()
    if teacher_info is None:
        return render_template('teacher/teacher_dashboard.html', teacher=None, courses=[])
    
    my_courses = Course.query.filter_by(teacher_id=teacher_info.id).all()
    return render_template('teacher/teacher_dashboard.html', teacher=teacher_info, courses=my_courses)

@teacher.route('/teacher/courses')
@login_required
def courses():
    if current_user.role != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    teacher_info = get_teacher_info()
    if not teacher_info:
        return redirect(url_for('teacher.dashboard'))
    
    my_courses = Course.query.filter_by(teacher_id=teacher_info.id).all()
    return render_template('teacher/course.html', courses=my_courses)

@teacher.route('/teacher/students')
@login_required
def students():
    if current_user.role != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    teacher_info = get_teacher_info()
    if not teacher_info:
        return redirect(url_for('teacher.dashboard'))
    
    # Get all students enrolled in teacher's courses
    my_courses = Course.query.filter_by(teacher_id=teacher_info.id).all()
    course_ids = [c.id for c in my_courses]
    enrollments = Enrollment.query.filter(Enrollment.course_id.in_(course_ids)).all()
    students_data = [e.student_id for e in enrollments]
    
    return render_template('teacher/course.html', enrollments=enrollments, courses=my_courses)

@teacher.route('/teacher/attendance')
@login_required
def attendance():
    if current_user.role != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    teacher_info = get_teacher_info()
    if not teacher_info:
        return redirect(url_for('teacher.dashboard'))
    
    my_courses = Course.query.filter_by(teacher_id=teacher_info.id).all()
    return render_template('teacher/attendance.html', courses=my_courses)

@teacher.route('/teacher/assignments')
@login_required
def assignments():
    if current_user.role != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    teacher_info = get_teacher_info()
    if not teacher_info:
        return redirect(url_for('teacher.dashboard'))
    
    my_courses = Course.query.filter_by(teacher_id=teacher_info.id).all()
    course_ids = [c.id for c in my_courses]
    assignments_data = Assignment.query.filter(Assignment.course_id.in_(course_ids)).all()
    
    return render_template('teacher/assignments.html', assignments=assignments_data, courses=my_courses)

@teacher.route('/teacher/grades')
@login_required
def grades():
    if current_user.role != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    teacher_info = get_teacher_info()
    if not teacher_info:
        return redirect(url_for('teacher.dashboard'))
    
    my_courses = Course.query.filter_by(teacher_id=teacher_info.id).all()
    return render_template('teacher/results.html', courses=my_courses)

# ==================== TEACHER API ENDPOINTS ====================

@teacher.route('/teacher/api/add-course', methods=['POST'])
@login_required
def add_course():
    """Add new course"""
    if current_user.role != 'teacher':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    teacher_info = get_teacher_info()
    if not teacher_info:
        return jsonify({'success': False, 'message': 'Teacher profile not found'}), 404
    
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        code = data.get('code', '').strip()
        
        if not name or not code:
            return jsonify({'success': False, 'message': 'Course name and code are required'}), 400
        
        # Check if course code already exists
        existing_course = Course.query.filter_by(code=code).first()
        if existing_course:
            return jsonify({'success': False, 'message': 'Course code already exists'}), 400
        
        course = Course(name=name, code=code, teacher_id=teacher_info.id)
        db.session.add(course)
        db.session.commit()
        
        flash(f'Course "{name}" added successfully!', 'success')
        return jsonify({'success': True, 'message': 'Course added successfully', 'course_id': course.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher.route('/teacher/api/update-course/<int:course_id>', methods=['PUT'])
@login_required
def update_course(course_id):
    """Update course details"""
    if current_user.role != 'teacher':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    teacher_info = get_teacher_info()
    if not teacher_info:
        return jsonify({'success': False, 'message': 'Teacher profile not found'}), 404
    
    try:
        course = Course.query.get(course_id)
        if not course or course.teacher_id != teacher_info.id:
            return jsonify({'success': False, 'message': 'Course not found'}), 404
        
        data = request.get_json()
        if 'name' in data:
            course.name = data['name']
        if 'code' in data:
            course.code = data['code']
        
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return jsonify({'success': True, 'message': 'Course updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher.route('/teacher/api/delete-course/<int:course_id>', methods=['DELETE'])
@login_required
def delete_course(course_id):
    """Delete course"""
    if current_user.role != 'teacher':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    teacher_info = get_teacher_info()
    if not teacher_info:
        return jsonify({'success': False, 'message': 'Teacher profile not found'}), 404
    
    try:
        course = Course.query.get(course_id)
        if not course or course.teacher_id != teacher_info.id:
            return jsonify({'success': False, 'message': 'Course not found'}), 404
        
        db.session.delete(course)
        db.session.commit()
        flash('Course deleted successfully!', 'success')
        return jsonify({'success': True, 'message': 'Course deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher.route('/teacher/api/mark-attendance', methods=['POST'])
@login_required
def mark_attendance():
    """Mark attendance for students"""
    if current_user.role != 'teacher':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    teacher_info = get_teacher_info()
    if not teacher_info:
        return jsonify({'success': False, 'message': 'Teacher profile not found'}), 404
    
    try:
        data = request.get_json()
        course_id = data.get('course_id')
        attendance_data = data.get('attendance', {})
        
        course = Course.query.get(course_id)
        if not course or course.teacher_id != teacher_info.id:
            return jsonify({'success': False, 'message': 'Course not found'}), 404
        
        # Mark attendance for each student
        for student_id, status in attendance_data.items():
            attendance = Attendance(
                student_id=student_id,
                course_id=course_id,
                date=date.today(),
                status=status
            )
            db.session.add(attendance)
        
        db.session.commit()
        flash('Attendance marked successfully!', 'success')
        return jsonify({'success': True, 'message': 'Attendance marked'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher.route('/teacher/api/add-assignment', methods=['POST'])
@login_required
def add_assignment():
    """Add new assignment"""
    if current_user.role != 'teacher':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    teacher_info = get_teacher_info()
    if not teacher_info:
        return jsonify({'success': False, 'message': 'Teacher profile not found'}), 404
    
    try:
        data = request.get_json()
        course_id = data.get('course_id')
        title = data.get('title', '').strip()
        due_date_str = data.get('due_date', '')
        
        course = Course.query.get(course_id)
        if not course or course.teacher_id != teacher_info.id:
            return jsonify({'success': False, 'message': 'Course not found'}), 404
        
        if not title:
            return jsonify({'success': False, 'message': 'Assignment title is required'}), 400
        
        due_date = datetime.fromisoformat(due_date_str) if due_date_str else None
        
        assignment = Assignment(course_id=course_id, title=title, due_date=due_date)
        db.session.add(assignment)
        db.session.commit()
        
        flash('Assignment added successfully!', 'success')
        return jsonify({'success': True, 'message': 'Assignment added', 'assignment_id': assignment.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher.route('/teacher/api/add-grade', methods=['POST'])
@login_required
def add_grade():
    """Add grade for student"""
    if current_user.role != 'teacher':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    teacher_info = get_teacher_info()
    if not teacher_info:
        return jsonify({'success': False, 'message': 'Teacher profile not found'}), 404
    
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        course_id = data.get('course_id')
        marks = float(data.get('marks', 0))
        total = float(data.get('total', 100))
        
        course = Course.query.get(course_id)
        if not course or course.teacher_id != teacher_info.id:
            return jsonify({'success': False, 'message': 'Course not found'}), 404
        
        # Check if grade already exists
        existing_grade = Grade.query.filter_by(student_id=student_id, course_id=course_id).first()
        
        if existing_grade:
            existing_grade.marks = marks
            existing_grade.total = total
        else:
            grade = Grade(student_id=student_id, course_id=course_id, marks=marks, total=total)
            db.session.add(grade)
        
        db.session.commit()
        flash('Grade added successfully!', 'success')
        return jsonify({'success': True, 'message': 'Grade added'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500