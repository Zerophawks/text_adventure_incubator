## auth.py
from flask_login import LoginManager, login_user, logout_user
from .models import User, db
from werkzeug.security import check_password_hash

# Initialize Flask-Login
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """
    Load a user given the user ID.
    
    :param user_id: The ID of the user to load.
    :return: The User object if found, None otherwise.
    """
    return User.query.get(int(user_id))

class AuthError(Exception):
    """
    Custom exception class to handle authentication errors.
    """
    def __init__(self, message):
        super().__init__(message)

def authenticate_user(username, password):
    """
    Authenticate a user by their username and password.
    
    :param username: The username of the user.
    :param password: The password of the user.
    :return: User object if authentication is successful.
    :raises AuthError: If authentication fails.
    """
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return user
    raise AuthError("Invalid username or password")

def logout():
    """
    Log out the current user.
    """
    logout_user()

def register_user(username, email, password):
    """
    Register a new user with the given username, email, and password.
    
    :param username: The username of the new user.
    :param email: The email of the new user.
    :param password: The password of the new user.
    :return: User object if registration is successful.
    :raises AuthError: If registration fails due to existing user.
    """
    if User.query.filter((User.username == username) | (User.email == email)).first():
        raise AuthError("Username or email already exists")

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def init_auth(app):
    """
    Initialize the authentication system by setting up the login manager.
    
    :param app: The Flask application object.
    """
    login_manager.init_app(app)
    login_manager.login_view = 'login'
