__author__ = 'jdomsic'

import cpuNode as CPU
import humidityNode as HUM
import lightNode as LIG
import temperatureNode as TMP


class Core(object):
    def __init__(self, name='default'):
        self.name = name
        self.nodes = []
        self.time = 0

    def init(self, nodes):
        self.nodes.extend(nodes)

    def collect(self):
        measurements = []
        for node in self.nodes:
            node.update()
            measurements.append(node.get())

        return measurements

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
