#!/usr/bin/python

__author__ = 'jdomsic'

"""
     Mocks a CORE.
     (1) Creates a CORE from STDIN data.
     (2) Sends core_data to WIZARD.

"""

import json
import random
import string
import sys
import traceback

TIME = 1430839235


class CoreMessage():
    def __init__(self, unique_id, module_type, value, timestamp):
        self.id = unique_id
        self.module = module_type
        self.value = value
        self.timestamp = timestamp

    def validate(self):
        assert type(self.id) is str and self.id != ''

    def get(self):
        return self.__dict__


def main():
    global TIME

    msgs = []
    for module in MODULES:
        rand_id = module
        sensor_value = random.randint(int(VALUES[0]), int(VALUES[1]))
        module_type = TYPE
        ts = int(TIME)

        msg = CoreMessage(rand_id, module_type, sensor_value, ts).get()
        msgs.append(msg)

    TIME += 1

    print json.dumps({'id': APP_ID, 'data': msgs})


def create_random_string(size):
    choices = string.ascii_letters
    return ''.join(random.choice(choices) for _ in range(size))


if __name__ == '__main__':
    try:
        APP_ID = sys.argv[1]
        TYPE = sys.argv[2]
        MODULES = sys.argv[3].split(',')
        VALUES = sys.argv[4].split(',')

        while True:
            main()

    except Exception as e:
        import traceback

        traceback.print_exc()
        print >>sys.stderr, str(e)
