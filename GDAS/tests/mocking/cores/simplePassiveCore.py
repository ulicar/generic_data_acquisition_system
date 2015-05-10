#!/usr/bin/python

__author__ = 'jdomsic'


import json
import httplib
import sys

from flask import Flask
from flask import Response

from simpleCore import Core
from sensorNodes import cpuNode
from sensorNodes import humidityNode
from sensorNodes import lightNode
from sensorNodes import temperatureNode

DUMMY = 0
sensors = [
    temperatureNode.TemperatureNode('termo01', 'temperature', DUMMY, DUMMY),
    temperatureNode.TemperatureNode('termo03', 'temperature', DUMMY, DUMMY),
    temperatureNode.TemperatureNode('termo04', 'temperature', DUMMY, DUMMY),

    humidityNode.HumidityNode('humidity01', 'humidity', DUMMY, DUMMY),
    humidityNode.HumidityNode('humidity01', 'humidity', DUMMY, DUMMY),

    cpuNode.CpuNode('cpu01', 'cpu', DUMMY, DUMMY),
    cpuNode.CpuNode('cpu02', 'cpu', DUMMY, DUMMY),

    lightNode.LightNode('light01', 'light', DUMMY, DUMMY),
    lightNode.LightNode('light02', 'light', DUMMY, DUMMY)
]

c = Core(name=sys.argv[1])
c.init(nodes=sensors)

TOKEN = 'aaaaaAAAAAaaaaa'
app = Flask(__name__)


@app.route('/default', methods=['GET'])
def query():

    """
    if 'Token' not in request.headers:
        return Response(response='No authentification token in http headers',
                        status=httplib.UNAUTHORIZED)

    if not request.headers.get('Token') == TOKEN:
        return Response(response='Incorrect token',
                        status=httplib.FORBIDDEN
    )
    """
    data = [{
        'core': c.name,
        'data': c.collect()
    }]

    return Response(
        mimetype='application/json',
        response=json.dumps(data),
        status=httplib.OK,
    )

if __name__ == '__main__':
    app.run(debug=False)
