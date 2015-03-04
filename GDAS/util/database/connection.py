__author__ = 'jdomsic'

from pymongo import Connection


def connect_to_db(app):
    host, port = app.config['DATABASE']
    return Connection(host, port)
