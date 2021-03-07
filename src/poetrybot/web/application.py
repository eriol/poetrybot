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

    r = jsonify(payload)
    r.status_code = status_code

    return r


@app.route("/poets", methods=["GET"])
def get_poets():

    s = store.session()
    poets = s.query(Poet).all()
    store.session.remove()

    return jsonify(poets)
