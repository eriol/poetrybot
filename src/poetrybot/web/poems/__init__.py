from flask import Blueprint

bp = Blueprint("poems", __name__)

from . import routes
