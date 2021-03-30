from flask import jsonify, request
from marshmallow import ValidationError

from poetrybot.database import store
from poetrybot.database.models import User

from ..errors import error

from . import bp
from .schemas import UserSchema, UserEditSchema

user_edit_schema = UserEditSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@bp.route("", methods=["GET"])
def get_users():

    with store.get_session() as s:
        users = s.query(User).all()

    return jsonify(users_schema.dump(users))


@bp.route("", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}

    try:
        data = user_schema.load(data)
    except ValidationError as err:
        return error(400, err.messages)

    created = None
    with store.get_session() as s:
        if s.query(User).filter(User.id == data["id"]).first():
            return error(400, "user with the specified id already exists")

        user = User(**data)
        s.add(user)
        s.commit()

        created = user_schema.dump(user)

    response = jsonify(created)
    response.status_code = 201
    return response


@bp.route("/<int:id>", methods=["GET"])
def get_user(id):

    with store.get_session() as s:
        user = s.query(User).filter(User.id == id).first()

    if not user:
        return error(404)

    return jsonify(user_schema.dump(user))


@bp.route("/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json() or {}

    try:
        data = user_edit_schema.load(data)
    except ValidationError as err:
        return error(400, err.messages)

    updated = None
    with store.get_session() as s:
        user = s.query(User).filter(User.id == id).first()

        if not user:
            return error(404)

        user.name = data["name"]
        s.commit()

        updated = user_schema.dump(user)

    return jsonify(updated)
