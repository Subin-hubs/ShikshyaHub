from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.recipe import Recipe
from app.models.comment import Comment
from app.models.user import User
import os
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@user_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    # Get recommended recipes (approved recipes from other users)
    recommended_recipes = Recipe.query.filter(
        Recipe.status == 'approved',
        Recipe.user_id != current_user.id
    ).order_by(Recipe.created_at.desc()).limit(6).all()
    
    # Get user's recipe count
    user_recipes_count = Recipe.query.filter_by(user_id=current_user.id).count()
    
    # Get user's comments count
    user_comments_count = Comment.query.filter_by(user_id=current_user.id).count()
    
    return render_template('user/dashboard.html', 
                         recommended_recipes=recommended_recipes,
                         recipes_count=user_recipes_count,
                         comments_count=user_comments_count)

@user_bp.route('/upload-recipe', methods=['GET', 'POST'])
@login_required
def upload_recipe():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        cooking_time = request.form.get('cooking_time')
        servings = request.form.get('servings')
        difficulty = request.form.get('difficulty')
        category = request.form.get('category')
        
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid duplicates
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        # Create recipe
        recipe = Recipe(
            user_id=current_user.id,
            title=title,
            description=description,
            ingredients=ingredients,
            steps=steps,
            cooking_time=int(cooking_time) if cooking_time else None,
            servings=int(servings) if servings else None,
            difficulty=difficulty,
            category=category,
            image=image_filename,
            status='pending'
        )
        
        db.session.add(recipe)
        db.session.commit()
        
        flash('Recipe uploaded successfully! It will be visible after admin approval.', 'success')
        return redirect(url_for('user.my_recipes'))
    
    return render_template('user/upload_recipe.html')

@user_bp.route('/my-recipes')
@login_required
def my_recipes():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(Recipe.created_at.desc()).all()
    return render_template('user/my_recipes.html', recipes=recipes)

@user_bp.route('/explore')
@login_required
def explore():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    # Get all approved recipes
    recipes = Recipe.query.filter_by(status='approved').order_by(Recipe.created_at.desc()).all()
    return render_template('user/explore.html', recipes=recipes)

@user_bp.route('/recipe/<int:recipe_id>')
@login_required
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Only show approved recipes to regular users (unless it's their own recipe)
    if not current_user.is_admin() and recipe.status != 'approved' and recipe.user_id != current_user.id:
        flash('Recipe not found or not yet approved.', 'warning')
        return redirect(url_for('user.explore'))
    
    comments = Comment.query.filter_by(recipe_id=recipe_id).order_by(Comment.created_at.desc()).all()
    return render_template('user/recipe_detail.html', recipe=recipe, comments=comments)

@user_bp.route('/recipe/<int:recipe_id>/comment', methods=['POST'])
@login_required
def add_comment(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    comment_text = request.form.get('comment')
    
    if comment_text:
        comment = Comment(
            recipe_id=recipe_id,
            user_id=current_user.id,
            comment=comment_text
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    
    return redirect(url_for('user.recipe_detail', recipe_id=recipe_id))

@user_bp.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Check if user owns this recipe
    if recipe.user_id != current_user.id:
        flash('You can only edit your own recipes.', 'danger')
        return redirect(url_for('user.my_recipes'))
    
    if request.method == 'POST':
        recipe.title = request.form.get('title')
        recipe.description = request.form.get('description')
        recipe.ingredients = request.form.get('ingredients')
        recipe.steps = request.form.get('steps')
        recipe.cooking_time = int(request.form.get('cooking_time')) if request.form.get('cooking_time') else None
        recipe.servings = int(request.form.get('servings')) if request.form.get('servings') else None
        recipe.difficulty = request.form.get('difficulty')
        recipe.category = request.form.get('category')
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Delete old image if exists
                if recipe.image:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], recipe.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                recipe.image = filename
        
        recipe.status = 'pending'  # Reset to pending after edit
        db.session.commit()
        
        flash('Recipe updated successfully! It will need re-approval.', 'success')
        return redirect(url_for('user.my_recipes'))
    
    return render_template('user/edit_recipe.html', recipe=recipe)

@user_bp.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Check if user owns this recipe
    if recipe.user_id != current_user.id:
        flash('You can only delete your own recipes.', 'danger')
        return redirect(url_for('user.my_recipes'))
    
    # Delete image if exists
    if recipe.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], recipe.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(recipe)
    db.session.commit()
    
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('user.my_recipes'))

@user_bp.route('/comments')
@login_required
def my_comments():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    comments = Comment.query.filter_by(user_id=current_user.id).order_by(Comment.created_at.desc()).all()
    return render_template('user/comments.html', comments=comments)

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        
        # Handle password change
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if current_password and new_password:
            if not current_user.check_password(current_password):
                flash('Current password is incorrect.', 'danger')
                return render_template('user/profile.html')
            
            if new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
                return render_template('user/profile.html')
            
            if len(new_password) < 6:
                flash('Password must be at least 6 characters long.', 'danger')
                return render_template('user/profile.html')
            
            current_user.set_password(new_password)
            flash('Password updated successfully!', 'success')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))
    
    return render_template('user/profile.html')
