from flask import jsonify, request
from marshmallow import ValidationError

from poetrybot.database import store
from poetrybot.database.models import User

from ..errors import error

from . import bp
from .schemas import UserSchema

user_schema = UserSchema()


@bp.route("", methods=["GET"])
def get_users():

    with store.get_session() as s:
        users = s.query(User).all()

    return jsonify([user.to_dict() for user in users])


@bp.route("", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}

    try:
        data = user_schema.load(data)
    except ValidationError as err:
        return error(400, err.messages)

    created = None
    with store.get_session() as s:
        if s.query(User).filter(User.id == data["id"]).one():
            return error(400, "user with the specified id already exists")

        user = User(**data)
        s.add(user)
        s.commit()

        created = user.to_dict()

    response = jsonify(created)
    response.status_code = 201
    return response
