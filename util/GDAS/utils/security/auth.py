__author__ = 'jdomsic'

import hashlib

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

    def authentificate(self, username, password):
        if not username or not password:
            return False

        self.db.open('gdas', 'accounts')
        query = {
            'username': username
        }

        user_info = self.db.get_record(query)
        if not user_info:
            return False

        self.user = username
        self.user_roles = user_info['roles']
        self.password = user_info['password']

        if self.password != hashlib.sha1(password).hexdigest() + \
                hashlib.sha1(username).hexdigest():

            return False

        return True

    def authorize(self, required_roles):
        for role in required_roles:
            if role not in self.user_roles:
                return False

        return True

    def is_admin(self, username, password):
        if username == 'gdas' and self.authentificate(username, password):
            return True

        return False


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
