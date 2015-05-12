#!/usr/bin/python

__author__ = 'jdomsic'

"""
    Mocks (strange hehe) counter sensor.
    
    Prints out multiple values in one sensor data (changed) every second.
    (Could be seen as weight of 3 (alien) fish in a aquarium, every second)
"""

import json
import time

from itertools import cycle

from sensorNode import SensorNode

UPDATE = cycle([(x, x % 45,  x // 11) for x in range(0, 190)])


class CounterNode(SensorNode):
    def __init__(self, unique_id, module_type, value, timestamp):
        super(self.__class__, self).\
            __init__(unique_id, module_type, value, timestamp)

    def update(self):
        self.update_value(int(time.time()), next(UPDATE))


if __name__ == '__main__':
    DUMMY = 0
    sensor = CounterNode('bagCounter', 'counter', DUMMY, DUMMY)
    sensor.validate()

    while True:
        sensor.update()

        print json.dumps(sensor.get(), indent=4)
        time.sleep(0.99)
