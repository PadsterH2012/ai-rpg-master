from datetime import datetime
from app import db

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    ollama_response = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    alignment = db.Column(db.String(20), nullable=False)
    player_class = db.Column(db.String(20), nullable=False)
    race = db.Column(db.String(20), nullable=False)
    pp = db.Column(db.Integer, default=0)
    gp = db.Column(db.Integer, default=0)
    sp = db.Column(db.Integer, default=0)
    cp = db.Column(db.Integer, default=0)
    hp = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    inventory = db.Column(db.Text, default="")
