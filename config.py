import os
from dotenv import load_dotenv

# This loads the secrets from your .env file
load_dotenv()

class Config:
    # A secret key keeps your website's forms safe from hackers
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # This tells Flask where your database is located
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # This folder will store uploaded assignments
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max file size: 16MB