__author__ = 'jdomsic'

from flask import request
from flask import Response

from functools import wraps

from GDAS.utils.database.connection import Fatty


class UserAuth(object):
    def __init__(self):
        self.db = Fatty()
        self.user = None
        self.password = None

        self.user_roles = None

    def authentificate(self, auth):
        if not auth and not auth.username and not auth.password:
            return False

        self.db.open('accounts')
        user_info = self.db.read(auth.username)
        if not user_info:
            return False

        self.user = auth.username
        self.user_roles = user_info['roles']
        self.password = user_info['password']

        if self.password != auth.password:
            return False

        return True

    def authorize(self, required_roles):
        if self.user == 'gdas':
            return True

        for role in required_roles:
            if role not in self.user_roles:
                return False

        return True


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
