__author__ = 'jdomsic'

import json
import random
import requests
import string
import sys
import time


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
    TIME = 1430839235

    while True:
        core = [
            (create_random_string(5), 'temperature', random.randint(-10, 5), TIME),
            (create_random_string(5), 'temperature', random.randint(0, 10), TIME),
            (create_random_string(5), 'humidity',    random.randint(80, 90), TIME),
            (create_random_string(5), 'humidity',    random.randint(70, 90), TIME),
            (create_random_string(5), 'cpu',         random.randint(50, 60), TIME),
            (create_random_string(5), 'cpu',         random.randint(50, 60), TIME),
            (create_random_string(5), 'cpu',         random.randint(50, 60), str(TIME)),
            (create_random_string(5), 'temperature', str(random.randint(-10, 5)), TIME),
            (create_random_string(5), 'temperature', str(random.randint(-10, 5)), TIME)
        ]

        msgs = []
        for msg in core:
            APP_ID = 'CORE'
            rand_id = msg[0]
            module_type = msg[1]
            sensor_value = msg[2]

            msg = CoreMessage(APP_ID, rand_id, module_type, sensor_value, TIME).get()
            msgs.append(msg)

        TIME += 1
        send_request(msgs)


def create_random_string(size):
    choices = string.ascii_letters
    return ''.join(random.choice(choices) for _ in range(size))


def send_request(data):
    requests.request(
        method='POST',
        headers={'Connection': 'close'},
        url="http://jdomsic:jdomsic@127.0.0.1:5000/wizard/upload",
        data=json.dumps(data)
    )


if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        import traceback

        traceback.print_exc()
        print >>sys.stderr, str(e)
