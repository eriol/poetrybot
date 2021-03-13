from flask import Flask

from .poets import bp as poets_bp
from .poems import bp as poems_bp

app = Flask(__name__)
app.register_blueprint(poets_bp, url_prefix="/poets")
app.register_blueprint(poems_bp, url_prefix="/poems")
