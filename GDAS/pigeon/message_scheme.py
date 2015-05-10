__author__ = 'jdomsic'


def create_message_scheme():
    """ message on the RabbitMq. It's received in Wizard or from active Core"""
    schema = {
        'type': 'array',
        'items': {
            'type': create_core_scheme()
        },
        "additionalProperties": False,
    }

    return schema


def create_core_scheme():
    """ Message created by a single Core whose name is in 'core' """
    schema = {
        'type': 'object',
        'properties': {
            'core': {'type': 'string'},
            'data': {'type': create_sensor_scheme()},
            },
        "patternProperties": {
            "^.+$": {'type': 'any'}
            },
        "additionalProperties": False,
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
        "patternProperties": {
            "^.+$": {'type': 'any'}
            },
        "additionalProperties": False,
        'required': ['id', 'value', 'timestamp', 'module']
    }

    return schema
