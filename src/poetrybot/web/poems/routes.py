from flask import jsonify, request
from marshmallow import ValidationError

from poetrybot.database import store
from poetrybot.database.models import Poem

from ..errors import error
from . import bp
from .schemas import PoemSchema

poem_schema = PoemSchema()
poems_schema = PoemSchema(many=True)


@bp.route("", methods=["GET"])
def get_poems():

    with store.get_session() as s:
        poems = s.query(Poem).all()

    return jsonify(poems_schema.dump(poems))


@bp.route("", methods=["POST"])
def create_poem():
    data = request.get_json(silent=True) or {}

    try:
        data = poem_schema.load(data)
    except ValidationError as err:
        return error(400, err.messages)

    created = None
    with store.get_session() as s:

        poem = Poem(**data)
        s.add(poem)
        s.commit()

        created = poem_schema.dump(poem)

    response = jsonify(created)
    response.status_code = 201
    return response


@bp.route("/<int:id>", methods=["GET"])
def get_poem(id):

    with store.get_session() as s:
        poem = s.query(Poem).filter(Poem.id == id).first()

    if not poem:
        return error(404)

    return jsonify(poem_schema.dump(poem))


@bp.route("/<int:id>", methods=["PUT"])
def update_poem(id):
    data = request.get_json(silent=True) or {}

    try:
        data = poem_schema.load(data)
    except ValidationError as err:
        return error(400, err.messages)

    updated = None
    with store.get_session() as s:
        poem = s.query(Poem).filter(Poem.id == id).first()

        if not poem:
            return error(404)

        for key in data:
            setattr(poem, key, data[key])
        s.commit()

        updated = poem_schema.dump(poem)

    return jsonify(updated)


@bp.route("/<int:id>", methods=["DELETE"])
def delete_poem(id):

    with store.get_session() as s:
        poem = s.query(Poem).filter(Poem.id == id).first()

        if not poem:
            return error(404)

        s.delete(poem)
        s.commit()

    return "", 204
