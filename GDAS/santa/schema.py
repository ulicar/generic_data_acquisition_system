__author__ = 'jdomsic'

from timemodule import utc_to_time_key


def crete_post_data_scheme():
    """ Message created by a single Core whose name is in 'core' """
    schema = {
        'type': 'object',
        'properties': {
            'user':  {'type: string'},
            'cores': {
                'type': 'array',
                'items': 'string'
            },
            'modules':  {
                'type': 'array',
                'items': 'string'
            },
            'time': {
                'type': 'object',
                'properties': {
                    'from': {'type': 'string'},
                    'to': {'type': 'string'}
                }
            }
        },
        'required': ['user', 'cores', 'modules', 'time']
    }

    return schema


def map_keys(schema, post_data):
    required_flag = False
    DATABASE = None
    if 'user' in post_data:
        required_flag = True
        DATABASE = post_data['user']

    COLLECTIONS = None
    if 'cores' in post_data:
        required_flag = True
        COLLECTIONS = post_data['cores'][:]

    if not required_flag:
        raise TypeError('Required one of: user, cores.')

    WHITELISTED_MODULES = None
    if 'modules' in post_data:
        if post_data['modules'] == '*':
            WHITELISTED_MODULES = []

        elif len(post_data['modules']) > 0:
            WHITELISTED_MODULES = post_data['modules'][:]

        else:
            raise TypeError('Error in field: modules ')

    TIME_START = None
    TIME_END = None
    if 'time' not in post_data:
        raise TypeError('Error in field: time')

    try:
        TIME_START = utc_to_time_key(post_data['time']['from'])
        TIME_END = utc_to_time_key(post_data['time']['to'])

    except (ValueError, TypeError):
        raise TypeError('Erorr in filed: time')

    return DATABASE, COLLECTIONS, WHITELISTED_MODULES, TIME_START, TIME_END