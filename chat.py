## chat.py
from datetime import datetime
from .models import db, Message

class ChatManager:
    def __init__(self, chat_room):
        self.chat_room = chat_room

    def post_message(self, user, text):
        """
        Posts a message to the chat room.

        :param user: The user sending the message.
        :param text: The text of the message.
        """
        new_message = Message(sender=user, text=text, chat_room=self.chat_room)
        db.session.add(new_message)
        db.session.commit()

    def get_recent_messages(self, limit=50):
        """
        Retrieves recent messages from the chat room.

        :param limit: The maximum number of messages to retrieve.
        :return: A list of the most recent messages.
        """
        return self.chat_room.messages.order_by(Message.timestamp.desc()).limit(limit).all()

    def get_messages_since(self, timestamp):
        """
        Retrieves messages from the chat room that were posted after the given timestamp.

        :param timestamp: The timestamp to filter messages.
        :return: A list of messages posted after the timestamp.
        """
        return self.chat_room.messages.filter(Message.timestamp > timestamp).order_by(Message.timestamp.asc()).all()
