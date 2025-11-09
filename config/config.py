"""
Configuration settings for Smart Surveillance System
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_APP = os.getenv('FLASK_APP', 'run.py')
    
    # Database Settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///surveillance.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Session Settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File Upload Settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    DETECTED_EVENTS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'detected_events')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'jpg', 'jpeg', 'png'}
    
    # Roboflow API Settings
    ROBOFLOW_API_KEY = os.getenv('ROBOFLOW_API_KEY', '')
    ROBOFLOW_WORKSPACE = os.getenv('ROBOFLOW_WORKSPACE', '')
    ROBOFLOW_PROJECT = os.getenv('ROBOFLOW_PROJECT', '')
    ROBOFLOW_VERSION = int(os.getenv('ROBOFLOW_VERSION', 1))
    ROBOFLOW_WORKFLOW_ID = os.getenv('ROBOFLOW_WORKFLOW_ID', 'detect-count-and-visualize')
    MAX_FPS = int(os.getenv('MAX_FPS', 30))
    
    # Email Settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '')
    ALERT_EMAIL_RECIPIENT = os.getenv('ALERT_EMAIL_RECIPIENT', '')
    
    # Camera Settings
    CAMERA_SOURCE = os.getenv('CAMERA_SOURCE', '0')
    MAX_CAMERAS = int(os.getenv('MAX_CAMERAS', 4))
    
    # Detection Settings
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.5))
    DETECTION_CLASSES = os.getenv('DETECTION_CLASSES', 'person,car,truck,bicycle,motorcycle').split(',')
    FRAME_SKIP = int(os.getenv('FRAME_SKIP', 2))
    
    # Video Settings
    MAX_VIDEO_CLIP_DURATION = int(os.getenv('MAX_VIDEO_CLIP_DURATION', 10))
    RETENTION_DAYS = int(os.getenv('RETENTION_DAYS', 30))
    VIDEO_FPS = 20
    VIDEO_WIDTH = 640
    VIDEO_HEIGHT = 480
    
    # Logging Settings
    LOG_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    LOG_FILE = os.path.join(LOG_FOLDER, 'app.log')
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # SocketIO Settings
    SOCKETIO_MESSAGE_QUEUE = None
    SOCKETIO_ASYNC_MODE = 'eventlet'
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.DETECTED_EVENTS_FOLDER, exist_ok=True)
        os.makedirs(Config.LOG_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to syslog in production
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists(cls.LOG_FOLDER):
            os.makedirs(cls.LOG_FOLDER)
        
        file_handler = RotatingFileHandler(
            cls.LOG_FILE,
            maxBytes=cls.LOG_MAX_BYTES,
            backupCount=cls.LOG_BACKUP_COUNT
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Smart Surveillance System startup')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
