from flask import jsonify, request
from marshmallow import ValidationError

from poetrybot.database import store
from poetrybot.database.models import Poet

from ..errors import error
from . import bp
from .schemas import PoetSchema

poet_schema = PoetSchema()
poets_schema = PoetSchema(many=True)


@bp.route("", methods=["GET"])
def get_poets():

    with store.get_session() as s:
        poets = s.query(Poet).all()

    return jsonify(poets_schema.dump(poets))


@bp.route("", methods=["POST"])
def create_poet():
    data = request.get_json() or {}

    try:
        data = poet_schema.load(data)
    except ValidationError as err:
        return error(400, err.messages)

    created = None
    with store.get_session() as s:

        if s.query(Poet).filter(Poet.name == data["name"]).first():
            return error(400, "this poet is already present")

        poet = Poet(name=data["name"])
        s.add(poet)
        s.commit()

        created = poet_schema.dump(poet)

    response = jsonify(created)
    response.status_code = 201
    return response


@bp.route("/<int:id>", methods=["GET"])
def get_poet(id):

    with store.get_session() as s:
        poet = s.query(Poet).filter(Poet.id == id).first()

    if not poet:
        return error(404)

    return jsonify(poet_schema.dump(poet))


@bp.route("/<int:id>", methods=["PUT"])
def update_poet(id):
    data = request.get_json() or {}

    try:
        data = poet_schema.load(data)
    except ValidationError as err:
        return error(400, err.messages)

    updated = None
    with store.get_session() as s:
        poet = s.query(Poet).filter(Poet.id == id).first()

        if not poet:
            return error(404)

        poet.name = data["name"]
        s.commit()

        updated = poet_schema.dump(poet)

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
