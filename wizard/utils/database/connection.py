__author__ = 'jdomsic'

from pymongo import Connection
from initialize import app

def get_db_connection():
    name = app.cfg.db[0]
    port = app.cfg.db[1]

    return Connection(name, port)
