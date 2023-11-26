## main.py
from flask import Flask
from .config import SECRET_KEY, DEBUG, SQLALCHEMY_DATABASE_URI, OPENAI_API_KEY, SOCKETIO_MESSAGE_QUEUE, REMEMBER_COOKIE_DURATION, PERMANENT_SESSION_LIFETIME
from .database import db, init_db
from .auth import init_auth
from .views import app as views_blueprint

app = Flask(__name__)

# Configuration setup
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['OPENAI_API_KEY'] = OPENAI_API_KEY
app.config['SOCKETIO_MESSAGE_QUEUE'] = SOCKETIO_MESSAGE_QUEUE
app.config['REMEMBER_COOKIE_DURATION'] = REMEMBER_COOKIE_DURATION
app.config['PERMANENT_SESSION_LIFETIME'] = PERMANENT_SESSION_LIFETIME

# Initialize database
db.init_app(app)
with app.app_context():
    init_db()

# Initialize authentication
init_auth(app)

# Register blueprints
app.register_blueprint(views_blueprint)

if __name__ == '__main__':
    app.run()
