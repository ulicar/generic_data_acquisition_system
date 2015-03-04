__author__ = 'jdomsic'

from pymongo import Connection


class Fatty(object):
    def __init__(self, db):
        self.host, self.port = db

    def open(self):
        return Connection(self.host, self.port)

    def read(self):
        pass

    def write(self):
        pass
