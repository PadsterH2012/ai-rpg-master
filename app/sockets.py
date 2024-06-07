import logging
from flask_socketio import emit
from app import socketio, db
from app.models import Conversation
from app.utils import player_interaction_agent
from datetime import datetime
import threading
import time
import pynvml

# Initialize NVML (NVIDIA Management Library)
pynvml.nvmlInit()

logger = logging.getLogger(__name__)

@socketio.on('message')
def handle_message(msg):
    user_message = msg['data']
    logger.info(f"Received user message: {user_message}")
    
    try:
        new_conversation = Conversation(user_message=user_message, timestamp=datetime.utcnow())
        db.session.add(new_conversation)
        db.session.commit()
        logger.info(f"User message saved: {user_message}")

        # Logging before making the request to Ollama API
        logger.debug(f"Requesting response from Ollama for message: {user_message}")

        overseer_response, story_update = player_interaction_agent(user_message)
        
        # Logging after receiving the response from Ollama API
        logger.info(f"Overseer response: {overseer_response}")
        logger.info(f"Story update: {story_update}")

        new_conversation.ollama_response = overseer_response
        db.session.add(new_conversation)
        db.session.commit()
        logger.info("Overseer response saved")

        story_conversation = Conversation(user_message="Story Update", ollama_response=story_update, timestamp=datetime.utcnow())
        db.session.add(story_conversation)
        db.session.commit()
        logger.info("Story update saved")

        emit('response', {
            'user_message': user_message,
            'ollama_response': overseer_response,
            'timestamp': new_conversation.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }, broadcast=True)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error handling message: {e}")
        emit('response', {'error': 'An error occurred while processing your message.'})


def fetch_gpu_load():
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    while True:
        gpu_utilization = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        logger.debug(f"GPU Utilization: {gpu_utilization}")
        socketio.emit('gpu_load', {'gpu_load': gpu_utilization})
        time.sleep(5)

# Start a separate thread to fetch GPU load periodically
threading.Thread(target=fetch_gpu_load, daemon=True).start()
