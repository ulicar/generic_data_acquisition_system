__author__ = 'jdomsic'

from pymongo import MongoClient


class Fatty(object):
    def __init__(self, db=('localhost', '29027')):
        self.host, self.port = db
        self.collection = None

    def open(self, collection):
        self.collection = MongoClient(self.host, self.port)[collection]

    def close(self):
        self.collection = None

    def read(self, query):
        data = self.collection.find(query)

        return data

    def write(self, data):
        self.collection.insert(data)
