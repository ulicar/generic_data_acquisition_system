__author__ = 'jdomsic'

from simpleCore import Core
from sensorNodes.cpuNode import CpuNode
from sensorNodes.counterNode import CounterNode
from sensorNodes.doorNode import DoorNode
from sensorNodes.humidityNode import HumidityNode
from sensorNodes.lightNode import LightNode
from sensorNodes.temperatureNode import TemperatureNode


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
            'temperature': TemperatureNode,
            'light': LightNode,
            'cpu': CpuNode,
            'humidity': HumidityNode,
            'counter': CounterNode,
            'door': DoorNode
        }[sensor_type]

        core_sensors.extend(get_sensors_by_type(parser, name, sensor_type, sensor_map))

    return core_sensors


def get_sensors_by_type(parser, name, sensor_type, sensor_map):
    dummy = 0  # get_dummy_value(sensor_type)
    sensors = list()
    for name in parser.get(name, sensor_type).strip().split(','):
        sensor = sensor_map(
            unique_id=name,
            module_type=sensor_type,
            value=dummy,
            timestamp=0
        )

        sensors.append(sensor)

    return sensors


def get_dummy_value(sensor_type):
    return {
        'temperature': 0,
        'light': 0,
        'cpu': (0, 0),
        'humidity': 0
    }[sensor_type]
