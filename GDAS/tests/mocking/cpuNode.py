__author__ = 'jdomsic'

import json
import time

from itertools import cycle

from sensorNode import SensorNode

UPDATE = cycle([x for x in range(50, 100)])


class CpuNode(SensorNode):
    def __init__(self, unique_id, module_type, value, timestamp):
        super(self.__class__, self).\
            __init__(unique_id, module_type, value, timestamp)

    def update(self):
        self.update_value(int(time.time()), next(UPDATE))


if __name__ == '__main__':
    DUMMY = 0
    sensor = CpuNode('cpu01', 'cpu', DUMMY, DUMMY)
    sensor.validate()

    while True:
        sensor.update()

        print json.dumps(sensor.get())
        time.sleep(0.99)
