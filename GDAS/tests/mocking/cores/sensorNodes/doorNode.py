#!/usr/bin/python

__author__ = 'jdomsic'

"""
    Mocks door sensor (open / closed).
    
    Prints out door sensor data (changed) every second.
"""

import json
import time

from random import random

from sensorNode import SensorNode


class DoorNode(SensorNode):
    def __init__(self, unique_id, module_type, value, timestamp):
        super(self.__class__, self).\
            __init__(unique_id, module_type, value, timestamp)

    def update(self):
        self.update_value(int(time.time()), random() > 0.5)


if __name__ == '__main__':
    DUMMY = 0
    sensor = DoorNode('Doors01', 'door', DUMMY, DUMMY)
    sensor.validate()

    while True:
        sensor.update()

        print json.dumps(sensor.get(), indent=4)
        time.sleep(0.99)
