__author__ = 'jdomsic'

import json


class Envelope(object):
    def __init__(self, data, data_type):
        self.MAPPER = {
            'DATA': data,
            'TYPE': data_type
        }

    def __str__(self):
        return json.dumps(self.MAPPER)

    @staticmethod
    def unpack(string):
        mapper = json.loads(string)
        return mapper['DATA'], mapper['TYPE']

