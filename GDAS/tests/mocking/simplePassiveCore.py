#!/usr/bin/python

__author__ = 'jdomsic'


import json
import httplib

from flask import Flask
from flask import Response
from flask import request

from simpleActiveCore import Core
import cpuNode as CPU
import humidityNode as HUM
import lightNode as LIG
import temperatureNode as TMP

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

@app.route('/core', methods=['GET'])
def query():

    if 'Token' not in request.headers:
        header = {'WWW-Authenticate': 'Basic realm=\"Core ' + c.name + 'sensor data.\"'}
        return Response(response='', status=httplib.UNAUTHORIZED, headers=header)

    if not request.headers.get('Token') == TOKEN:
        return Response(response='Not allowed for this user', status=httplib.FORBIDDEN)

    data = [{
        'core': c.name,
        'data': c.collect()
    }]

    return Response(response=json.dumps(data), status=httplib.OK)


if __name__ == '__main__':
    app.run(debug=True)
