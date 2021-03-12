from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


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
