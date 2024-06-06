from flask import Blueprint, render_template, request, jsonify, current_app as app
from app.models import Conversation, db
from app.utils import player_interaction_agent
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    conversations = Conversation.query.order_by(Conversation.timestamp.asc()).all()
    return render_template('chat.html', conversations=conversations)

@main.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "Message content is required"}), 400

    try:
        new_conversation = Conversation(user_message=user_message, timestamp=datetime.utcnow())
        db.session.add(new_conversation)
        db.session.commit()
        app.logger.info(f"User message saved: {user_message}")

        overseer_response, story_update = player_interaction_agent(user_message)
        app.logger.info(f"Overseer response: {overseer_response}")
        app.logger.info(f"Story update: {story_update}")

        new_conversation.ollama_response = overseer_response
        db.session.add(new_conversation)
        db.session.commit()
        app.logger.info("Overseer response saved")

        story_conversation = Conversation(user_message="Story Update", ollama_response=story_update, timestamp=datetime.utcnow())
        db.session.add(story_conversation)
        db.session.commit()
        app.logger.info("Story update saved")

        return jsonify({
            "user_message": user_message,
            "overseer_response": overseer_response,
            "story_update": story_update,
            "timestamp": new_conversation.timestamp
        })
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error handling message: {e}")
        return jsonify({"error": "An error occurred while processing your message."}), 500

@main.route('/full_conversation')
def full_conversation():
    conversations = Conversation.query.order_by(Conversation.timestamp.asc()).all()
    conversations_data = [
        {
            'user_message': conv.user_message,
            'ollama_response': conv.ollama_response,
            'timestamp': conv.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for conv in conversations
    ]
    return jsonify({'conversations': conversations_data})
