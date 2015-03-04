__author__ = 'jdomsic'

from flask import request
from flask import Response

from functools import wraps


def authentificate(app, db_client):
    return True
    # TODO:
    master_db = db_client['master']


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return Response('Missing username/password', 401,
                            {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated


def requires_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.json:
            return Response('Accepts only Content-Type: application/json', 400)
        return f(*args, **kwargs)
    return decorated


def authorize(username, required_roles, db):
    return True # TODO: debug

    user_roles = get_roles_for_user(username, db)
    for role in required_roles:
        if role not in user_roles:
            return False

    return True


def get_roles_for_user(username, db):
    return ['upload']