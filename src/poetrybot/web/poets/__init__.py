from flask import Blueprint

bp = Blueprint("poets", __name__)

from poetrybot.web.poets import routes
