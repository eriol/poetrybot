from flask import Flask, request

from poetrybot.config import Config
from poetrybot.database import store

from .poets import bp as poets_bp
from .poems import bp as poems_bp


def create_app(config=None):
    """Create a Flask app with specified configuration.

    If config is None the configuration is made using environment variables.
    """
    if config is None:
        config = Config.from_environ()
    store.connect(config.DATABASE_URL)

    app = Flask(__name__)

    @app.before_request
    def check_auth_token():
        """Check every request for the Authorization header."""
        auth_token = request.headers.get("Authorization")

        if auth_token != config.AUTH_TOKEN:
            return "", 401

    app.register_blueprint(poets_bp, url_prefix="/poets")
    app.register_blueprint(poems_bp, url_prefix="/poems")

    return app
