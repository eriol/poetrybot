from flask import jsonify, request

from poetrybot.database import store
from poetrybot.database.models import Poem

from . import bp
from ..errors import error


@bp.route("", methods=["GET"])
def get_poems():

    with store.get_session() as s:
        poems = s.query(Poem).all()

    return jsonify([poem.to_dict() for poem in poems])


@bp.route("", methods=["POST"])
def create_poem():
    data = request.get_json() or {}

    if "verses" not in data:
        return error(400, "verses field is required")
    if data["verses"] == "":
        return error(400, "verses field can't be empty")

    created = None
    with store.get_session() as s:

        poet = Poem()
        s.add(poet)
        s.commit()

        created = poet.to_dict()

    response = jsonify(created)
    response.status_code = 201
    return response
