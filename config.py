# Kisan+ Configuration

import os
from datetime import timedelta

class Config:
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///kisan.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # API Keys (set these in environment variables for production)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
    
    # Features flags
    ENABLE_VOICE_FEATURES = True
    ENABLE_OFFLINE_MODE = True
    ENABLE_NOTIFICATIONS = True
    
    # Languages supported
    SUPPORTED_LANGUAGES = [
        ('en', 'English'),
        ('hi', 'हिंदी'), 
        ('te', 'తెలుగు'),
        ('ta', 'தமிழ்'),
        ('kn', 'ಕನ್ನಡ'),
        ('ml', 'മലയാളം'),
        ('mr', 'मराठी'),
        ('gu', 'ગુજરાતી'),
        ('pa', 'ਪੰਜਾਬੀ'),
        ('bn', 'বাংলা')
    ]

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
