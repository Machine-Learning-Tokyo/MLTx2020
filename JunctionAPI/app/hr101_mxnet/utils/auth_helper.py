from functools import wraps
from flask import request, jsonify


def check_auth(username, password):
    """This function is called to check if a username password combination is valid."""
    return username == 'MLT' and \
           password == 'junction_tokyo'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    message = {
        'info': {
            'message': 'Could not verify the credentials',
            'code': 15
        }
    }

    return jsonify(message), 401


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
