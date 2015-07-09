__author__ = 'jdomsic'
import json

class message_data_t():
    name = None
    time = None
    data = dict()

    def __init__(self):
        pass

    def fill(self, raw_data):
        for entry in raw_data:
            key, value = entry
            self.data[key] = value

    def __str__(self):
        return json.dumps([self.name, self.data])
