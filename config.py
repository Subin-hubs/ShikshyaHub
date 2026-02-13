import os
from dotenv import load_dotenv

# This loads the secrets from your .env file
load_dotenv()

BASEDIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASEDIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)


class Config:
    # A secret key keeps your website's forms safe from hackers
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard-to-guess-string"

    # This tells Flask where your database is located
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        "sqlite:///" + os.path.join(INSTANCE_DIR, "shikshyahub.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # This folder will store uploaded assignments
    UPLOAD_FOLDER = os.path.join(BASEDIR, "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max file size: 16MB