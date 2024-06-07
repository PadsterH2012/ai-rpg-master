from app import create_app, socketio
import logging

app = create_app()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug("Starting Flask-SocketIO server")
    socketio.run(app, host='0.0.0.0', port=5000)
