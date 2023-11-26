## views.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import db, User, Adventure, ChatRoom, Message, GameSession
from .forms import LoginForm, RegistrationForm, AdventureCreationForm, StoryPromptForm, MessageForm
from .auth import authenticate_user, logout as auth_logout, register_user
from .game_manager import GameManager
from .chat import ChatManager

app = Flask(__name__)
app.config.from_object('config')

# Initialize database
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = register_user(form.username.data, form.email.data, form.password.data)
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = authenticate_user(form.username.data, form.password.data)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout_view():
    auth_logout()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/adventure/create', methods=['GET', 'POST'])
@login_required
def create_adventure():
    form = AdventureCreationForm()
    if form.validate_on_submit():
        game_manager = GameManager(current_user)
        adventure = game_manager.create_adventure(form.title.data)
        flash('Adventure created successfully!', 'success')
        return redirect(url_for('view_adventure', adventure_id=adventure.id))
    return render_template('create_adventure.html', form=form)

@app.route('/adventure/<int:adventure_id>')
@login_required
def view_adventure(adventure_id):
    adventure = Adventure.query.get_or_404(adventure_id)
    return render_template('view_adventure.html', adventure=adventure)

@app.route('/adventure/<int:adventure_id>/chat', methods=['GET', 'POST'])
@login_required
def adventure_chat(adventure_id):
    adventure = Adventure.query.get_or_404(adventure_id)
    chat_room = adventure.chat_room
    form = MessageForm()
    chat_manager = ChatManager(chat_room)
    if form.validate_on_submit():
        chat_manager.post_message(current_user, form.message.data)
        form.message.data = ''
    messages = chat_manager.get_recent_messages()
    return render_template('adventure_chat.html', adventure=adventure, form=form, messages=messages)

@app.route('/adventure/<int:adventure_id>/play', methods=['GET', 'POST'])
@login_required
def play_adventure(adventure_id):
    adventure = Adventure.query.get_or_404(adventure_id)
    form = StoryPromptForm()
    game_manager = GameManager(current_user)
    if form.validate_on_submit():
        game_manager.generate_and_update_story(adventure_id, form.prompt.data)
        flash('Story updated successfully!', 'success')
    return render_template('play_adventure.html', adventure=adventure, form=form)

@app.route('/adventure/<int:adventure_id>/join')
@login_required
def join_adventure(adventure_id):
    game_manager = GameManager(current_user)
    try:
        game_manager.join_adventure(adventure_id, current_user)
        flash('Joined adventure successfully!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('view_adventure', adventure_id=adventure_id))

@app.route('/adventure/<int:adventure_id>/leave')
@login_required
def leave_adventure(adventure_id):
    game_manager = GameManager(current_user)
    try:
        game_manager.leave_adventure(adventure_id, current_user)
        flash('Left adventure successfully!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('view_adventure', adventure_id=adventure_id))

# Additional routes can be added here

if __name__ == '__main__':
    app.run()
