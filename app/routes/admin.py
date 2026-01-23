from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Student, Teacher, Course

admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    # Count how many of each we have for the dashboard stats
    stats = {
        'users': User.query.count(),
        'students': Student.query.count(),
        'teachers': Teacher.query.count(),
        'courses': Course.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin.route('/admin/manage-users')
@login_required
def manage_users():
    all_users = User.query.all()
    return render_template('admin/manage_users.html', users=all_users)