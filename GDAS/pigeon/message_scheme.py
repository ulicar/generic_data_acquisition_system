__author__ = 'jdomsic'


def create_core_scheme():
    """ Message created by a single Core whose name is in 'core' """
    schema = {
        'type': 'object',
        'properties': {
            'core': {'type': 'string'},
            'data': {
                'type': 'array',
                'items': create_sensor_scheme(),
            },
        },
        'required': ['core', 'data']
    }

    return schema


def create_sensor_scheme():
    """ Sensor value """
    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'string'},
            'value': {'type': 'any'},
            'timestamp': {'type': 'integer'},
            'module': {'type': 'string'}
            },
        'required': ['id', 'value', 'timestamp', 'module']
    }

    return schema
