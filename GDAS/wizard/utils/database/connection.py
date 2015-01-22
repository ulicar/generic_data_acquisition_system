__author__ = 'jdomsic'

from pymongo import Connection
from initialize import app

def get_db_connection():
    name = app.cfg.database[0]
    port = app.cfg.database[1]

    return Connection(name, port)
