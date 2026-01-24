from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Teacher, Course, Attendance

teacher = Blueprint('teacher', __name__)

@teacher.route('/teacher/dashboard')
@login_required
def dashboard():
    # Only let teachers access this page
    if current_user.role != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    # Get teacher specific data
    teacher_info = Teacher.query.filter_by(user_id=current_user.id).first()
    
    # FIX: If teacher profile doesn't exist yet, show a welcome state
    if teacher_info is None:
        return render_template('teacher/dashboard.html', teacher=None, courses=[])

    # If profile exists, get their courses
    my_courses = Course.query.filter_by(teacher_id=teacher_info.id).all()
    return render_template('teacher/dashboard.html', teacher=teacher_info, courses=my_courses)

@teacher.route('/teacher/courses')
@login_required
def courses():
    teacher_info = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher_info:
        flash('Teacher profile not found.', 'warning')
        return redirect(url_for('teacher.dashboard'))
    my_courses = Course.query.filter_by(teacher_id=teacher_info.id).all()
    return render_template('teacher/courses.html', courses=my_courses)