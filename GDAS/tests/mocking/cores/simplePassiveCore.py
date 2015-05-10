#!/usr/bin/python

__author__ = 'jdomsic'


import ConfigParser
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


def create_cores(parser):
    cores = dict()
    for name in parser.get('core', 'apps').strip().split(','):
        core = Core(name=name)
        cores[name] = core
        core_sensors = create_sensors(parser, name)
        core.init(nodes=core_sensors)

    return cores


def create_sensors(parser, name):
    core_sensors = list()
    for sensor_type in parser.get(name, 'sensors').strip().split(','):
        sensor_map = {
            'temperature': temperatureNode.TemperatureNode,
            'light': lightNode.LightNode,
            'cpu': cpuNode.CpuNode,
            'humidity': humidityNode.HumidityNode
        }[sensor_type]

        core_sensors.extend(get_sensors_by_type(parser, name, sensor_type, sensor_map))

    return core_sensors


def get_sensors_by_type(parser, name, sensor_type, sensor_map):
    dummy = 0
    sensors = list()
    for name in parser.get(name, sensor_type).strip().split(','):
        sensor = sensor_map(
            name,
            sensor_type,
            dummy,
            dummy
        )

        sensors.append(sensor)

    return sensors


TOKEN = 'aaaaaAAAAAaaaaa'
app = Flask(__name__)
parser = ConfigParser.ConfigParser()
parser.read(sys.argv[1])
cores = create_cores(parser)


@app.route('/<core_name>/fetch', methods=['GET'])
def query(core_name):
    if core_name not in cores:
        return Response(response='No core by that name',
                        status=httplib.BAD_REQUEST
        )

    """
    if 'Token' not in request.headers:
        return Response(response='No authentification token in http headers',
                        status=httplib.UNAUTHORIZED)

    if not request.headers.get('Token') == TOKEN:
        return Response(response='Incorrect token',
                        status=httplib.FORBIDDEN
    )
    """

    c = cores[core_name]
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
