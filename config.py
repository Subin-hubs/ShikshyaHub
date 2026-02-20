import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'flavorhive.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # eSewa Test Configuration
    ESEWA_MERCHANT_CODE = 'EPAYTEST'
    ESEWA_SUCCESS_URL = 'http://localhost:5000/payment/success'
    ESEWA_FAILURE_URL = 'http://localhost:5000/payment/failure'
    ESEWA_PAYMENT_URL = 'https://uat.esewa.com.np/epay/main'
