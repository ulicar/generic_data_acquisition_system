__author__ = 'jdomsic'

from pymongo import Connection


class Fatty(object):
    def __init__(self, db):
        self.host, self.port = db
        self.collection = None

    def open(self, collection):
        self.collection = Connection(self.host, self.port)[collection]

    def close(self):
        self.collection = None

    def read(self, query):
        data = self.collection.find(query)

        return data

    def write(self, data):
        self.collection.insert(data) #TODO make keys
