__author__ = 'jdomsic'


def create_message_scheme():
    schema = {
        'type': 'array',
        'items': {
            'type': create_sensor_scheme()
        },
        "additionalProperties": False,
    }

    return schema


def create_core_scheme():
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
    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'string'},
            'value': {'type': 'any'},
            'timestamp': {'type': 'integer'},
            'module': {'type': 'string'},
            'app_id': {'type': 'string'}
            },
        "patternProperties": {
            "^.+$": {'type': 'any'}
            },
        "additionalProperties": False,
        'required': ['id', 'value', 'timestamp', 'module', 'app_id']
    }

    return schema
