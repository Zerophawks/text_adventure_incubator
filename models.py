## models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    adventures = db.relationship('Adventure', backref='game_master', lazy='dynamic')

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_id(self) -> str:
        return str(self.id)

class Adventure(db.Model):
    __tablename__ = 'adventure'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    game_master_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    story_state = db.Column(db.PickleType, nullable=True)
    players = db.relationship('User', secondary='adventure_players', backref=db.backref('adventures_joined', lazy='dynamic'))

    def __init__(self, title: str, game_master: User):
        self.title = title
        self.game_master_id = game_master.id

    def add_player(self, player: User):
        if player not in self.players:
            self.players.append(player)

    def remove_player(self, player: User):
        if player in self.players:
            self.players.remove(player)

    def update_story_state(self, state: dict):
        self.story_state = state

class GameSession(db.Model):
    __tablename__ = 'game_session'
    id = db.Column(db.Integer, primary_key=True)
    adventure_id = db.Column(db.Integer, db.ForeignKey('adventure.id'), nullable=False)
    session_data = db.Column(db.PickleType, nullable=True)
    adventure = db.relationship('Adventure', backref=db.backref('session', uselist=False))

    def __init__(self, adventure: Adventure):
        self.adventure_id = adventure.id

    def save_session(self):
        db.session.commit()

    def load_session(self) -> dict:
        return self.session_data if self.session_data else {}

class OpenAIAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_story(self, prompt: str) -> str:
        # TODO: Implement integration with the OpenAI API to generate a story
        raise NotImplementedError("The generate_story method has not been implemented yet.")

class ChatRoom(db.Model):
    __tablename__ = 'chat_room'
    id = db.Column(db.Integer, primary_key=True)
    adventure_id = db.Column(db.Integer, db.ForeignKey('adventure.id'), nullable=False)
    adventure = db.relationship('Adventure', backref=db.backref('chat_room', uselist=False))
    messages = db.relationship('Message', backref='chat_room', lazy='dynamic')

    def __init__(self, adventure: Adventure):
        self.adventure_id = adventure.id

    def send_message(self, user: User, message: str):
        new_message = Message(sender=user, text=message)
        db.session.add(new_message)
        db.session.commit()

    def get_messages(self) -> list:
        return self.messages.all()

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    chat_room_id = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=False)

    def __init__(self, sender: User, text: str):
        self.sender_id = sender.id
        self.text = text

# Association table for the many-to-many relationship between Adventure and User
adventure_players = db.Table('adventure_players',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('adventure_id', db.Integer, db.ForeignKey('adventure.id'), primary_key=True)
)
