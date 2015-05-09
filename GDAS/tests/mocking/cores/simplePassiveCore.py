#!/usr/bin/python

__author__ = 'jdomsic'


import json
import httplib

from flask import Flask
from flask import Response
from flask import request

from simpleCore import Core
from sensorNodes import cpuNode as CPU
from sensorNodes import humidityNode as HUM
from sensorNodes import lightNode as LIG
from sensorNodes import temperatureNode as TMP

DUMMY = 0
sensors = [
    TMP.TemperatureNode('termo01', 'temperature', DUMMY, DUMMY),
    TMP.TemperatureNode('termo03', 'temperature', DUMMY, DUMMY),
    TMP.TemperatureNode('termo04', 'temperature', DUMMY, DUMMY),

    HUM.HumidityNode('humidity01', 'humidity', DUMMY, DUMMY),
    HUM.HumidityNode('humidity01', 'humidity', DUMMY, DUMMY),

    CPU.CpuNode('cpu01', 'cpu', DUMMY, DUMMY),
    CPU.CpuNode('cpu02', 'cpu', DUMMY, DUMMY),

    LIG.LightNode('light01', 'light', DUMMY, DUMMY),
    LIG.LightNode('light02', 'light', DUMMY, DUMMY)
]

c = Core('default')
c.init(nodes=sensors)

TOKEN = 'aaaaaAAAAAaaaaa'
app = Flask(__name__)

@app.route('/core/default', methods=['GET'])
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
