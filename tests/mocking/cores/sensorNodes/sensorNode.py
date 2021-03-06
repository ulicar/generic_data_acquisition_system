__author__ = 'jdomsic'

"""
    Mocks a generic sensor.
    
    Prints out temperature sensor data (changed) every second.
    (Same as child class TemperatureNode from temperatureNode.py)
"""


class SensorNode(object):
    def __init__(self, unique_id, module_type, value, timestamp):
        self.id = unique_id
        self.module = module_type
        self.value = value
        self.timestamp = timestamp

    def validate(self):
        assert type(self.id) is str and self.id != ''
        assert type(self.timestamp) is int
        assert self.module is not None
        assert self.value is not None

    def get(self):
        return self.__dict__

    def update_value(self, timestamp, value):
        self.value = value
        self.timestamp = timestamp

if __name__ == '__main__':
    import json
    import time

    DUMMY = 0
    sensor = SensorNode('zxy44', 'temperature', DUMMY, DUMMY)
    sensor.validate()

    while True:
        TIME = int(time.time())

        sensor.update_value(timestamp=TIME, value=TIME % 50)

        print json.dumps(sensor.get(), indent=4)
        time.sleep(0.99)
