import logging

from flask import Flask

from app.audio.routes import router as audio_router


logging.basicConfig(level=logging.DEBUG)


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(audio_router)

    return app
