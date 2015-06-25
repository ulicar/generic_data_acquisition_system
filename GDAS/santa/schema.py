__author__ = 'jdomsic'

from timemodule import to_datetime


def create_post_data_scheme():
    """ Message created by a single Core whose name is in 'core' """
    schema = {
        "type": "object",
        "properties": {
        "user": {
            "type": "string"
        },
        "modules": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "core": {
            "type": "string",
        },
        "time": {
          "type": "object",
          "properties": {
            "from": {
              "type": "string"
            },
            "to": {
              "type": "string"
            }
          }
        }
      },
      "required": [
        "user",
        "modules",
        "core",
        "time"
      ]
    }

    return schema


def map_keys(post_data):
    database = post_data['user']
    collections = post_data['core']
    modules = post_data['modules'][:]

    try:
        time_start = to_datetime(post_data['time']['from'])
        time_end = to_datetime(post_data['time']['to'])

    except (ValueError, TypeError) as e:
        raise TypeError('Error in field: time')

    return database, collections, modules, time_start, time_end
