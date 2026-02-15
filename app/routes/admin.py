from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.recipe import Recipe
from app.models.user import User
from app.models.comment import Comment
from app.models.payment import Payment
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get statistics
    total_users = User.query.filter_by(role='user').count()
    total_recipes = Recipe.query.count()
    pending_recipes = Recipe.query.filter_by(status='pending').count()
    approved_recipes = Recipe.query.filter_by(status='approved').count()
    total_comments = Comment.query.count()
    total_payments = Payment.query.filter_by(status='success').count()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).filter_by(status='success').scalar() or 0
    
    # Recent recipes
    recent_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_recipes=total_recipes,
                         pending_recipes=pending_recipes,
                         approved_recipes=approved_recipes,
                         total_comments=total_comments,
                         total_payments=total_payments,
                         total_revenue=total_revenue,
                         recent_recipes=recent_recipes)

@admin_bp.route('/recipes')
@login_required
@admin_required
def recipes():
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'all':
        recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    else:
        recipes = Recipe.query.filter_by(status=status_filter).order_by(Recipe.created_at.desc()).all()
    
    return render_template('admin/recipes.html', recipes=recipes, status_filter=status_filter)

@admin_bp.route('/recipe/<int:recipe_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe.status = 'approved'
    db.session.commit()
    flash(f'Recipe "{recipe.title}" has been approved!', 'success')
    return redirect(url_for('admin.recipes'))

@admin_bp.route('/recipe/<int:recipe_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe.status = 'rejected'
    db.session.commit()
    flash(f'Recipe "{recipe.title}" has been rejected.', 'warning')
    return redirect(url_for('admin.recipes'))

@admin_bp.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Delete image if exists
    if recipe.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], recipe.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(recipe)
    db.session.commit()
    
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('admin.recipes'))

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.filter_by(role='user').order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.is_admin():
        flash('Cannot delete admin users.', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/comments')
@login_required
@admin_required
def comments():
    all_comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('admin/comments.html', comments=all_comments)

@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    
    flash('Comment deleted successfully!', 'success')
    return redirect(url_for('admin.comments'))

@admin_bp.route('/payments')
@login_required
@admin_required
def payments():
    all_payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template('admin/payments.html', payments=all_payments)

@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@admin_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        
        # Handle password change
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if current_password and new_password:
            if not current_user.check_password(current_password):
                flash('Current password is incorrect.', 'danger')
                return render_template('admin/profile.html')
            
            if new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
                return render_template('admin/profile.html')
            
            if len(new_password) < 6:
                flash('Password must be at least 6 characters long.', 'danger')
                return render_template('admin/profile.html')
            
            current_user.set_password(new_password)
            flash('Password updated successfully!', 'success')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin.profile'))
    
    return render_template('admin/profile.html')
