from flask import jsonify

from poetrybot.database import store
from poetrybot.database.models import User

from . import bp
from ..errors import error


@bp.route("", methods=["GET"])
def get_users():

    with store.get_session() as s:
        users = s.query(User).all()

    return jsonify([user.to_dict() for user in users])
