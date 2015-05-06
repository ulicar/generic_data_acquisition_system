__author__ = 'jdomsic'

from pymongo import MongoClient


class Fatty(object):
    def __init__(self, db=('localhost', 27017)):
        self.host, self.port = db
        self.collection = None

    def open(self, database, collection):
        self.collection = MongoClient(self.host, int(self.port))[database][collection]

    def close(self):
        self.collection = None

    def read(self, query):
        data = self.collection.find(query)

        return data

    def get_record(self, keys):
        assert isinstance(keys, dict), 'must be a key - value object'
        data = self.collection.find_one(keys)

        return data

    def write(self, data):
        self.collection.insert(data)

    def append(self, keys, values, create=True):
        assert isinstance(keys, dict), 'First argument must be dict'
        assert isinstance(values, dict), 'Second argument must be dict'
        assert isinstance(create, bool), 'Third argument must be bool'
        values = {
            '$set': values
        }

        self.collection.update(keys, values, upsert=create)
