__author__ = 'jdomsic'

from sensorNode import SensorNode


class Core(object):
    def __init__(self, name='default'):
        self.name = name
        self.nodes = []
        self.time = 0

    def init(self, nodes):
        for uniq_id, model, value in nodes:
            self.nodes.append(SensorNode(self.name, uniq_id, model, value, self.time))

    def collect(self):
        measurements = []
        for node in self.nodes:
            measurements.append(node.get())

            node.timestamp = self.time


if __name__ == '__main__':
    import json
    import time
    from testlib import create_random_value as rand

    nodes = [
        (rand('a', 5, str), 'temperature', rand(0, 10, int)),
        (rand('b', 5, str), 'temperature', rand(0, 10, int)),
        (rand('c', 5, str), 'humidity',    rand(80, 90, int)),
        (rand('d', 5, str), 'humidity',    rand(70, 90, int)),
        (rand('e', 5, str), 'cpu',         rand(50, 60, int)),
        (rand('f', 5, str), 'cpu',         rand(50, 60, int)),
        (rand('g', 5, str), 'cpu',         rand(50, 60, int)),
        (rand('i', 5, str), 'temperature', rand(-10, 5, str)),
        (rand('j', 5, str), 'temperature', rand(-5, 9, str))
    ]

    c = Core('default')
    c.init(nodes=nodes)
    while True:

        print json.dumps(c.collect())
