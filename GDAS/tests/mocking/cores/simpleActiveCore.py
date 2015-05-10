__author__ = 'jdomsic'


"""
    Mocks a CORE.

    Prints out all sensor data (changed) every second.
    (4x Temp, 3x Humidity, 2x Cpu, 2x Light senors.)
"""

import json
import sys
import time
import requests

from sensorNodes import cpuNode as CPU
from sensorNodes import humidityNode as HUM
from sensorNodes import lightNode as LIG
from sensorNodes import temperatureNode as TMP

from simpleCore import Core


def main():
    sensors = init_sensors()
    c = Core(name=sys.argv[1])
    c.init(nodes=sensors)

    PUSH = False
    if len(sys.argv) > 2 and sys.argv[2] == '--push':
        PUSH = True

    while True:
        data = json.dumps(c.collect())

        if PUSH:
            send_request(data)
            print 'Data sent to server.'

        else:
            print data

        time.sleep(0.99)


def init_sensors():
    DUMMY = 0
    sensors = [
        TMP.TemperatureNode('termo01', 'temperature', DUMMY, DUMMY),
        TMP.TemperatureNode('termo02', 'temperature', DUMMY, DUMMY),
        TMP.TemperatureNode('termo03', 'temperature', DUMMY, DUMMY),
        TMP.TemperatureNode('termo04', 'temperature', DUMMY, DUMMY),

        HUM.HumidityNode('humidity01', 'humidity', DUMMY, DUMMY),
        HUM.HumidityNode('humidity01', 'humidity', DUMMY, DUMMY),
        HUM.HumidityNode('humidity01', 'humidity', DUMMY, DUMMY),

        CPU.CpuNode('cpu01', 'cpu', DUMMY, DUMMY),
        CPU.CpuNode('cpu02', 'cpu', DUMMY, DUMMY),

        LIG.LightNode('light01', 'light', DUMMY, DUMMY),
        LIG.LightNode('light02', 'light', DUMMY, DUMMY)
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
        url="http://jdomsic:jdomsic@victim.no-ip.org/wizard/upload",
        data=data
    )

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()

        print >>sys.stderr, str(e)

