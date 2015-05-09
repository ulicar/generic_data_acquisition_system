__author__ = 'jdomsic'


"""
    Mocks a CORE.

    Prints out all sensor data (changed) every second.
    (4x Temp, 3x Humidity, 2x Cpu, 2x Light senors.)
"""

from sensorNodes import cpuNode as CPU
from sensorNodes import humidityNode as HUM
from sensorNodes import lightNode as LIG
from sensorNodes import temperatureNode as TMP

from simpleCore import Core

if __name__ == '__main__':
    import json
    import time

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

    c = Core('default')
    c.init(nodes=sensors)
    while True:
        print json.dumps(c.collect())

        time.sleep(0.99)
