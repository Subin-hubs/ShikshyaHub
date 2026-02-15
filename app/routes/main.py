from flask import Blueprint, render_template
from app.models.recipe import Recipe

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get some featured approved recipes for the landing page
    featured_recipes = Recipe.query.filter_by(status='approved').order_by(Recipe.created_at.desc()).limit(5).all()
    return render_template('index.html', featured_recipes=featured_recipes)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')
