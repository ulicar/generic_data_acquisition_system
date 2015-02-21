__author__ = 'jdomsic'

from pymongo import Connection

def get_db_connection(app):
    name = app.cfg.database[0]
    port = app.cfg.database[1]

    return Connection(name, port)
