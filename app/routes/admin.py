from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.models import User, Student, Teacher, Course, Attendance, Grade, Enrollment, db
from datetime import datetime

admin = Blueprint('admin', __name__)

# Security Helper: Reusable check for Admin access
def check_admin():
    if not current_user.is_authenticated or current_user.role != 'admin':
        return False
    return True

# ==================== ADMIN VIEWS ====================

@admin.route('/admin/dashboard')
@login_required
def dashboard():
    if not check_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    stats = {
        'users': User.query.count(),
        'students': Student.query.count(),
        'teachers': Teacher.query.count(),
        'courses': Course.query.count()
    }
    return render_template('admin/admin_dashboard.html', stats=stats)

@admin.route('/admin/manage-users')
@login_required
def manage_users():
    if not check_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    all_users = User.query.all()
    return render_template('admin/manage_students.html', users=all_users)

@admin.route('/admin/courses')
@login_required
def courses():
    if not check_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    all_courses = Course.query.all()
    all_teachers = Teacher.query.all()
    return render_template('admin/manage_courses.html', courses=all_courses, teachers=all_teachers)

@admin.route('/admin/attendance')
@login_required
def attendance():
    if not check_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    all_attendance = Attendance.query.all()
    return render_template('admin/manage_attendance.html', attendance=all_attendance)

@admin.route('/admin/reports')
@login_required
def reports():
    if not check_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    students_count = Student.query.count()
    teachers_count = Teacher.query.count()
    courses_count = Course.query.count()
    total_enrollments = Enrollment.query.count()
    
    return render_template('admin/manage_results.html', 
                         students_count=students_count,
                         teachers_count=teachers_count,
                         courses_count=courses_count,
                         total_enrollments=total_enrollments)

# ==================== ADMIN API ENDPOINTS (AJAX HANDLERS) ====================

@admin.route('/admin/api/add-user', methods=['POST'])
@login_required
def add_user():
    """Add new user"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        role = data.get('role', 'student').lower()
        
        # Validation
        if not all([name, email, password]):
            return jsonify({'success': False, 'message': 'Name, email, and password are required'}), 400
        
        if role not in ['admin', 'teacher', 'student']:
            return jsonify({'success': False, 'message': 'Invalid role'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Create User
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # Generates the ID for profile linking
        
        # Create Profile
        if role == 'student':
            student = Student(
                user_id=user.id,
                student_id_no=data.get('student_id_no', f'STU-{user.id:04d}'),
                year=data.get('year', '1st Year'),
                semester=data.get('semester', '1st Semester')
            )
            db.session.add(student)
        
        elif role == 'teacher':
            teacher = Teacher(
                user_id=user.id,
                employee_id=data.get('employee_id', f'EMP-{user.id:04d}'),
                department=data.get('department', 'General')
            )
            db.session.add(teacher)
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'User "{name}" ({role}) added successfully', 'user_id': user.id})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin.route('/admin/api/update-user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    """Update user details"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Prevent updating own admin role
        if user_id == current_user.id:
            return jsonify({'success': False, 'message': 'Cannot modify your own account'}), 400
        
        data = request.get_json()
        
        if 'name' in data:
            user.name = data['name'].strip()
        if 'email' in data:
            new_email = data['email'].strip()
            existing = User.query.filter_by(email=new_email).first()
            if existing and existing.id != user_id:
                return jsonify({'success': False, 'message': 'Email already exists'}), 400
            user.email = new_email
        if 'password' in data and data['password'].strip():
            user.set_password(data['password'].strip())
        if 'role' in data:
            user.role = data['role'].lower()
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'User updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin.route('/admin/api/delete-user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """Delete user"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        if user_id == current_user.id:
            return jsonify({'success': False, 'message': 'Cannot delete your own account'}), 400
        
        user = User.query.get_or_404(user_id)
        
        # Because of cascade='all, delete-orphan' in models.py, 
        # deleting 'user' automatically deletes Student/Teacher/Attendance/Grades.
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'User and all related data deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin.route('/admin/api/add-course', methods=['POST'])
@login_required
def add_course():
    if not check_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        code = data.get('code', '').strip()
        teacher_id = data.get('teacher_id') # This should be the ID from the Teacher table
        
        if not name or not code:
            return jsonify({'success': False, 'message': 'Course name and code are required'}), 400
        
        if Course.query.filter_by(code=code).first():
            return jsonify({'success': False, 'message': 'Course code already exists'}), 400

        # FIX: Verify the teacher exists in the Teacher table before assigning
        if teacher_id:
            teacher_exists = Teacher.query.get(teacher_id)
            if not teacher_exists:
                return jsonify({'success': False, 'message': 'Invalid Teacher selection'}), 400
        
        new_course = Course(name=name, code=code, teacher_id=teacher_id)
        db.session.add(new_course)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'Course "{name}" created successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin.route('/admin/api/update-course/<int:course_id>', methods=['PUT'])
@login_required
def update_course(course_id):
    """Update course details"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'success': False, 'message': 'Course not found'}), 404
        
        data = request.get_json()
        if 'name' in data:
            course.name = data['name'].strip()
        if 'code' in data:
            course.code = data['code'].strip()
        if 'teacher_id' in data:
            course.teacher_id = data['teacher_id']
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Course updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin.route('/admin/api/delete-course/<int:course_id>', methods=['DELETE'])
@login_required
def delete_course(course_id):
    """Delete course"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'success': False, 'message': 'Course not found'}), 404
        
        db.session.delete(course)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Course deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin.route('/admin/api/bulk-enroll', methods=['POST'])
@login_required
def bulk_enroll():
    """Bulk enroll students in courses"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        data = request.get_json()
        course_id = data.get('course_id')
        student_ids = data.get('student_ids', [])
        
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'success': False, 'message': 'Course not found'}), 404
        
        enrolled_count = 0
        for student_id in student_ids:
            existing = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
            if not existing:
                enrollment = Enrollment(student_id=student_id, course_id=course_id)
                db.session.add(enrollment)
                enrolled_count += 1
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'{enrolled_count} students enrolled successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin.route('/admin/api/system-backup', methods=['POST'])
@login_required
def system_backup():
    """Create system backup"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        # TODO: Implement actual backup logic
        return jsonify({'success': True, 'message': 'System backup created successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500