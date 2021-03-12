from flask import Flask

from .poets import bp as poets_bp

app = Flask(__name__)
app.register_blueprint(poets_bp, url_prefix="/poets")
