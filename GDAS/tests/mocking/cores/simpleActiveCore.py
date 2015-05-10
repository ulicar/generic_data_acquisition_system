#!/usr/bin/python

__author__ = 'jdomsic'


"""
    Mocks a CORE.

    Prints out all sensor data (changed) every second.
    (4x Temp, 3x Humidity, 2x Cpu, 2x Light senors.)
"""

import json
import sys
import requests

from sensorNodes import cpuNode
from sensorNodes import humidityNode
from sensorNodes import lightNode
from sensorNodes import temperatureNode

from simpleCore import Core


def main():
    sensors = init_sensors()
    c = Core(name=sys.argv[1])
    c.init(nodes=sensors)

    push_flag = False
    if len(sys.argv) > 2 and sys.argv[2] == '--push':
        push_flag = True

    while True:
        data = [{
            'core': c.name,
            'data': c.collect()
        }]

        if push_flag:
            send_request(json.dumps(data))
            print 'Data sent to server.'

        else:
            print data


def init_sensors():
    dummy = 0
    sensors = [
        temperatureNode.TemperatureNode('termo01', 'temperature', dummy, dummy),
        temperatureNode.TemperatureNode('termo02', 'temperature', dummy, dummy),
        temperatureNode.TemperatureNode('termo03', 'temperature', dummy, dummy),
        temperatureNode.TemperatureNode('termo04', 'temperature', dummy, dummy),

        humidityNode.HumidityNode('humidity01', 'humidity', dummy, dummy),
        humidityNode.HumidityNode('humidity01', 'humidity', dummy, dummy),
        humidityNode.HumidityNode('humidity01', 'humidity', dummy, dummy),

        cpuNode.CpuNode('cpu01', 'cpu', dummy, dummy),
        cpuNode.CpuNode('cpu02', 'cpu', dummy, dummy),

        lightNode.LightNode('light01', 'light', dummy, dummy),
        lightNode.LightNode('light02', 'light', dummy, dummy)
    ]

    return sensors


def send_request(data):
    auth_token = 'aaaaaAAAAAaaaaa'

    requests.request(
        method='POST',
        headers={
            'Connection': 'close',
            'token': auth_token,
            'Content-Type': 'application/json'
            },
        url="http://jdomsic:jdomsic@localhost:5000/upload",
        data=data
    )

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()

        print >>sys.stderr, str(e)
