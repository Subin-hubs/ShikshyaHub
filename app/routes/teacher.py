from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Teacher, Course, Assignment

teacher = Blueprint('teacher', __name__)

@teacher.route('/teacher/dashboard')
@login_required
def dashboard():
    if current_user.role != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
        
    teacher_info = Teacher.query.filter_by(user_id=current_user.id).first()
    my_courses = Course.query.filter_by(teacher_id=teacher_info.id).all()
    
    return render_template('teacher/dashboard.html', teacher=teacher_info, courses=my_courses)

@teacher.route('/teacher/my-classes')
@login_required
def my_classes():
    teacher_info = Teacher.query.filter_by(user_id=current_user.id).first()
    courses = Course.query.filter_by(teacher_id=teacher_info.id).all()
    return render_template('teacher/my_classes.html', courses=courses)