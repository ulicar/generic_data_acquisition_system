__author__ = 'jdomsic'

import json
import time

from itertools import cycle

from sensorNode import SensorNode

UPDATE = cycle([x * x * 0.3 for x in range(0, 20, 2)])


class LightNode(SensorNode):
    def __init__(self, app_id, unique_id, module_type, value, timestamp, optional=()):
        super(self.__class__, self).\
            __init__(app_id, unique_id, module_type, value, timestamp, optional)

    def update(self):
        self.update_value(int(time.time()), next(UPDATE))


if __name__ == '__main__':
    DUMMY = 0
    sensor = LightNode('Light sensor', 'light01', 'light', DUMMY, DUMMY)
    sensor.validate()

    while True:
        sensor.update()

        print json.dumps(sensor.get())
        time.sleep(0.99)
