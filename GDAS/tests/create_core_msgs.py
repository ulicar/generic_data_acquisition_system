#!/usr/bin/python

__author__ = 'jdomsic'

import json
import random
import string
import sys
import time
import traceback

TIME = 1430839235

APP_ID = sys.argv[1]
TYPE = sys.argv[2]
MODULES = sys.argv[3].split(',')
VALUES = sys.argv[4].split(',')


class AggregatorMessage():
    def __init__(self, dbID, name, ip, port, ports_path, ports_status, res_path, res_status, unique_id, time, err):
        self._id = dbID
        self.name = name
        self.ip = ip
        self.port = port
        self.ports = {'path': ports_path, 'status': ports_status}
        self.resources = {'path': res_path, 'status': res_status}
        self.id = unique_id
        self.timeout = time
        self.error = err

    def validate(self):
        assert type(self.id) is str and self.id != ''


class CoreMessage():
    def __init__(self, app_id, unique_id, module_type, value, timestamp, dbID=''):
        self.app_id = app_id
        self.id = unique_id
        #self._id = dbID
        self.module = module_type
        self.value = value
        self.timestamp = timestamp

    def validate(self):
        assert type(self.id) is str and self.id != ''

    def get(self):
        return self.__dict__

def main():
    msgs = []
    for _ in range(1, 10):
        rand_id = random.choice(MODULES)
        sensor_value = random.randint(int(VALUES[0]), int(VALUES[1]))
        module_type = TYPE
        ts = create_timestamp()
        time.sleep(0.2)

        msgs.append(CoreMessage(APP_ID, rand_id, sensor_value, module_type, ts))

    print json.dumps(msgs)


def create_timestamp():
    global TIME
    TIME += 1

    return str(TIME)


def create_random_string(size):
    choices = string.ascii_letters
    return ''.join(random.choice(choices) for _ in range(size))

if __name__ == '__main__':
    try:
        while True:
            main()

    except Exception as e:
        import traceback

        traceback.print_exc()
        print >>sys.stderr, str(e)
