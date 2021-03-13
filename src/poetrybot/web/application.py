from flask import Flask

from poetrybot.config import Config
from poetrybot.database import store

from .poets import bp as poets_bp
from .poems import bp as poems_bp


def create_app(config=None):
    if config is None:
        config = Config.from_environ()
    store.connect(config.DATABASE_URL)

    app = Flask(__name__)
    app.register_blueprint(poets_bp, url_prefix="/poets")
    app.register_blueprint(poems_bp, url_prefix="/poems")

    return app
