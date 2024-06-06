import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure the instance folder exists
    instance_path = os.path.join(Config.BASE_DIR, 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    # Configure logging
    log_dir = os.path.join(Config.BASE_DIR, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    handler = TimedRotatingFileHandler(
        os.path.join(log_dir, 'app.log'), 
        when="midnight", 
        interval=1
    )
    handler.suffix = "%Y-%m-%d"
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)

    app.logger.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
