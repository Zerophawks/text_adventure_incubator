## config.py
import os

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')  # Environment variable or default
DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 't']  # Convert to boolean

# Database configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///text_adventure_incubator.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# OpenAI API configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'default_openai_api_key')  # Environment variable or default

# Flask-SocketIO configuration
SOCKETIO_MESSAGE_QUEUE = os.environ.get('SOCKETIO_MESSAGE_QUEUE', 'redis://')

# Flask-Login configuration
REMEMBER_COOKIE_DURATION = int(os.environ.get('REMEMBER_COOKIE_DURATION', 3600))  # Duration in seconds

# Flask-Session configuration
PERMANENT_SESSION_LIFETIME = int(os.environ.get('PERMANENT_SESSION_LIFETIME', 3600))  # Duration in seconds

# Additional configurations can be added here as needed
