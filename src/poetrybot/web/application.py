from flask import Flask, jsonify, request
from werkzeug.http import HTTP_STATUS_CODES

from poetrybot.config import Config
from poetrybot.database import store
from poetrybot.database.models import Poet

app = Flask(__name__)
config = Config.from_environ()

store.connect(config.DATABASE_URL)


def error(status_code, message=None):
    """Return the error specified by the status_code.

    If message is present, attach also it to the response.
    """
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown")}
    if message:
        payload["message"] = message

    response = jsonify(payload)
    response.status_code = status_code

    return response


@app.route("/poets", methods=["GET"])
def get_poets():

    s = store.session()
    poets = s.query(Poet).all()
    store.session.remove()

    return jsonify([poet.to_dict() for poet in poets])


@app.route("/poets", methods=["POST"])
def create_poet():
    data = request.get_json() or {}

    if "name" not in data:
        return error(400, "name field is required")
    if data["name"] == "":
        return error(400, "name field can't be empty")

    s = store.session()

    if s.query(Poet).filter(Poet.name == data["name"]).first():
        return error(400, "this poet is already present")

    poet = Poet(name=data["name"])
    s.add(poet)
    s.commit()

    response = jsonify(poet.to_dict())
    response.status_code = 201
    return response
