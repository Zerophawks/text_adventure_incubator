## api.py
import openai
from flask import current_app
from .config import OPENAI_API_KEY
from .models import db, Adventure

class OpenAIAdapter:
    def __init__(self, api_key: str = OPENAI_API_KEY):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_story(self, prompt: str) -> str:
        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=150  # Assuming 150 is a sensible default
            )
            story = response.choices[0].text.strip() if response.choices else ""
            return story
        except openai.error.OpenAIError as e:
            current_app.logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {e}")
            raise

def update_adventure_story(adventure_id: int, prompt: str):
    """
    Updates the story state of an adventure using the OpenAI API.
    
    :param adventure_id: ID of the Adventure to be updated.
    :param prompt: The prompt to be sent to the OpenAI API.
    :return: None
    """
    adventure = Adventure.query.get(adventure_id)
    if adventure:
        openai_adapter = OpenAIAdapter()
        try:
            story_update = openai_adapter.generate_story(prompt)
            adventure.update_story_state({'story': story_update})
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Failed to update adventure story: {e}")
            # Consider re-raising the exception or handling it appropriately
