import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file
load_dotenv()

class Config(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No SQLALCHEMY_DATABASE_URI set for SQLAlchemy")
    
    # print(f'Database URL: {SQLALCHEMY_DATABASE_URI}')  # Debug print to ensure the URL is loaded

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    IMAGES_LOCATION = os.path.join(basedir, 'static', 'images')

    # Flask JWT extended
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'JWT_SUPER_SECRET')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=10)
    JWT_AUTH_USERNAME_KEY = 'username'
    JWT_AUTH_HEADER_PREFIX = 'Bearer'

    """  """
    # CORS
    CORS_ORIGIN_WHITELIST = [
        'http://localhost:4000',
        'http://localhost:5001',
    ]

    """  """
    # JWT_COOKIE_CSRF_PROTECT : False
    # WTF_CSRF_ENABLED = False

    # WTF_CSRF_CHECK_DEFAULT = False
    

# app = Flask(__name__)
# app.config.from_object(Config)

# db = SQLAlchemy(app)

# Rest of your Flask app setup
