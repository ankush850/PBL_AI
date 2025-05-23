from flask import Flask
from app.config import Config
from app.routes.main import main
from app.routes.pdf_routes import pdf
from app.routes.chat_routes import chat

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(pdf)
    app.register_blueprint(chat)

    return app