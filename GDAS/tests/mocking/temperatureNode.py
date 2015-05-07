__author__ = 'jdomsic'

import json
import time

from itertools import cycle

from sensorNode import SensorNode

UPDATE = cycle([x * 0.25 for x in range(0, 20)])


class TemperatureNode(SensorNode):
    def __init__(self, unique_id, module_type, value, timestamp, optional=()):
        super(self.__class__, self).\
            __init__( unique_id, module_type, value, timestamp, optional)

    def update(self):
        self.update_value(int(time.time()), next(UPDATE))


if __name__ == '__main__':
    DUMMY = 0
    sensor = TemperatureNode('termo01', 'temperature', DUMMY, DUMMY)
    sensor.validate()

    while True:
        sensor.update()

        print json.dumps(sensor.get())
        time.sleep(0.99)
