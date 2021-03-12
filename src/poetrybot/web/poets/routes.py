from flask import Flask, jsonify, request

from poetrybot.config import Config
from poetrybot.database import store
from poetrybot.database.models import Poet

from . import bp
from ..errors import error

config = Config.from_environ()

store.connect(config.DATABASE_URL)


@bp.route("/", methods=["GET"])
def get_poets():

    s = store.session()
    poets = s.query(Poet).all()
    store.session.remove()

    return jsonify([poet.to_dict() for poet in poets])


@bp.route("/", methods=["POST"])
def create_poet():
    data = request.get_json() or {}

    if "name" not in data:
        return error(400, "name field is required")
    if data["name"] == "":
        return error(400, "name field can't be empty")

    s = store.session()

    if s.query(Poet).filter(Poet.name == data["name"]).first():
        store.session.remove()
        return error(400, "this poet is already present")

    poet = Poet(name=data["name"])
    s.add(poet)
    s.commit()
    store.session.remove()

    response = jsonify(poet.to_dict())
    response.status_code = 201
    return response


@bp.route("/<int:poet_id>", methods=["GET"])
def get_poet(poet_id):

    s = store.session()
    poet = s.query(Poet).filter(Poet.id == poet_id).first()
    store.session.remove()

    if not poet:
        return error(404)

    return jsonify(poet.to_dict())
