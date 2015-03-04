__author__ = 'jdomsic'

import random
import string
import time
import json

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
    def __init__(self, unique_id, module_type, value, timestamp, dbID=''):
        self.id = unique_id
        #self._id = dbID
        self.module = module_type
        self.value = value
        self.timestamp = timestamp

    def validate(self):
        assert type(self.id) is str and self.id != ''

    def get(self):
        return self.__dict__


def create_random_string(size):
    choices = string.ascii_letters
    return ''.join(random.choice(choices) for _ in range(size))

def create_random_value(min, max):
    return random.randint(min, max)

def create_timestamp():
    return str(int(time.time()))

def create_random_core_message():
    rand_id = create_random_string(10)
    sensor_value = create_random_value(-10, 50)
    module_type = 'temperature'
    ts = create_timestamp()

    return CoreMessage(rand_id, module_type, sensor_value, ts).get()


msgs = []
for _ in range(1, 10):
    msgs.append(create_random_core_message())

print json.dumps(msgs)
