from flask import Flask, jsonify, request

from poetrybot.config import Config
from poetrybot.database import store
from poetrybot.database.models import Poet

from . import bp
from ..errors import error

config = Config.from_environ()

store.connect(config.DATABASE_URL)


@bp.route("", methods=["GET"])
def get_poets():

    with store.get_session() as s:
        poets = s.query(Poet).all()

    return jsonify([poet.to_dict() for poet in poets])


@bp.route("", methods=["POST"])
def create_poet():
    data = request.get_json() or {}

    if "name" not in data:
        return error(400, "name field is required")
    if data["name"] == "":
        return error(400, "name field can't be empty")

    created = None
    with store.get_session() as s:

        if s.query(Poet).filter(Poet.name == data["name"]).first():
            return error(400, "this poet is already present")

        poet = Poet(name=data["name"])
        s.add(poet)
        s.commit()

        created = poet.to_dict()

    response = jsonify(created)
    response.status_code = 201
    return response


@bp.route("/<int:id>", methods=["GET"])
def get_poet(id):

    with store.get_session() as s:
        poet = s.query(Poet).filter(Poet.id == id).first()

    if not poet:
        return error(404)

    return jsonify(poet.to_dict())


@bp.route("/<int:id>", methods=["PUT"])
def update_poet(id):
    data = request.get_json() or {}

    if "name" not in data:
        return error(400, "name field is required")
    if data["name"] == "":
        return error(400, "name field can't be empty")

    updated = None
    with store.get_session() as s:
        poet = s.query(Poet).filter(Poet.id == id).first()

        if not poet:
            return error(404)

        poet.name = data["name"]
        s.commit()

        updated = poet.to_dict()

    return jsonify(updated)


@bp.route("/<int:id>", methods=["DELETE"])
def delete_poet(id):

    with store.get_session() as s:
        poet = s.query(Poet).filter(Poet.id == id).first()

        if not poet:
            return error(404)

        s.delete(poet)
        s.commit()

    return "", 204
