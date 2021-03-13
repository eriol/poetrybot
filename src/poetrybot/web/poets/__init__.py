from flask import Blueprint

bp = Blueprint("poets", __name__)

from . import routes
