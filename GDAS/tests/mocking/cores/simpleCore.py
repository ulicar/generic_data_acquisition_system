#!/usr/bin/python

__author__ = 'jdomsic'


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
