from app import db
from datetime import datetime

class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(300))
    cooking_time = db.Column(db.Integer)  # in minutes
    servings = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    category = db.Column(db.String(50))  # breakfast, lunch, dinner, dessert, snack
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('Comment', backref='recipe', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Recipe {self.title}>'
