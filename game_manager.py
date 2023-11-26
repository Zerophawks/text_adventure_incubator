## game_manager.py
from .models import User, Adventure, GameSession, ChatRoom, db
from .api import update_adventure_story

class GameManager:
    def __init__(self, user: User):
        self.user = user

    def create_adventure(self, title: str) -> Adventure:
        new_adventure = Adventure(title=title, game_master=self.user)
        db.session.add(new_adventure)
        db.session.commit()
        return new_adventure

    def join_adventure(self, adventure_id: int, player: User):
        adventure = Adventure.query.get(adventure_id)
        if not adventure:
            raise ValueError(f"Adventure with ID {adventure_id} does not exist.")
        adventure.add_player(player)
        db.session.commit()

    def leave_adventure(self, adventure_id: int, player: User):
        adventure = Adventure.query.get(adventure_id)
        if not adventure:
            raise ValueError(f"Adventure with ID {adventure_id} does not exist.")
        adventure.remove_player(player)
        db.session.commit()

    def start_game_session(self, adventure_id: int) -> GameSession:
        adventure = Adventure.query.get(adventure_id)
        if not adventure:
            raise ValueError(f"Adventure with ID {adventure_id} does not exist.")
        new_session = GameSession(adventure=adventure)
        db.session.add(new_session)
        db.session.commit()
        return new_session

    def end_game_session(self, session_id: int):
        session = GameSession.query.get(session_id)
        if not session:
            raise ValueError(f"Game session with ID {session_id} does not exist.")
        db.session.delete(session)
        db.session.commit()

    def save_game_session(self, session_id: int):
        session = GameSession.query.get(session_id)
        if not session:
            raise ValueError(f"Game session with ID {session_id} does not exist.")
        session.save_session()

    def load_game_session(self, session_id: int) -> dict:
        session = GameSession.query.get(session_id)
        if not session:
            raise ValueError(f"Game session with ID {session_id} does not exist.")
        return session.load_session()

    def send_chat_message(self, chat_room_id: int, user: User, message: str):
        chat_room = ChatRoom.query.get(chat_room_id)
        if not chat_room:
            raise ValueError(f"Chat room with ID {chat_room_id} does not exist.")
        chat_room.send_message(user, message)

    def get_chat_messages(self, chat_room_id: int) -> list:
        chat_room = ChatRoom.query.get(chat_room_id)
        if not chat_room:
            raise ValueError(f"Chat room with ID {chat_room_id} does not exist.")
        return chat_room.get_messages()

    def generate_and_update_story(self, adventure_id: int, prompt: str):
        try:
            update_adventure_story(adventure_id, prompt)
        except Exception as e:
            raise RuntimeError(f"Failed to generate and update story: {e}")
