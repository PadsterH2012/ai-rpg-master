from flask_socketio import emit
from app import socketio, db
from app.models import Conversation
from app.utils import player_interaction_agent
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@socketio.on('message')
def handle_message(msg):
    user_message = msg['data']
    logger.debug(f"Received user message: {user_message}")
    
    try:
        new_conversation = Conversation(user_message=user_message, timestamp=datetime.utcnow())
        db.session.add(new_conversation)
        db.session.commit()
        logger.debug(f"User message saved: {user_message}")

        overseer_response, story_update = player_interaction_agent(user_message)
        logger.debug(f"Overseer response: {overseer_response}")
        logger.debug(f"Story update: {story_update}")

        new_conversation.ollama_response = overseer_response
        db.session.add(new_conversation)
        db.session.commit()
        logger.debug("Overseer response saved")

        story_conversation = Conversation(user_message="Story Update", ollama_response=story_update, timestamp=datetime.utcnow())
        db.session.add(story_conversation)
        db.session.commit()
        logger.debug("Story update saved")

        emit('response', {
            'user_message': user_message,
            'ollama_response': overseer_response,
            'timestamp': new_conversation.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }, broadcast=True)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error handling message: {e}")
        emit('response', {'error': 'An error occurred while processing your message.'})
