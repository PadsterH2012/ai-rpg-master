import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'chat.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OLLAMA_URL = "http://10.203.20.99:11434/api/generate"
    OLLAMA_MODEL = "llama3:8b-instruct-q8_0"
