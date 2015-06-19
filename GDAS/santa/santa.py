#!/usr/bin/python

__author__ = 'jdomsic'

import ConfigParser
import httplib
import logging
import json
import sys

from flask import Flask
from flask import Response
from flask import request
from validictory import validate

from schema import *
from timemodule import *
from GDAS.utils.security.auth import UserAuth


app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

APP_ID = config.get('gdas', 'app_id')
ROLES = config.get('santa', 'required_roles').split(',')
SCHEMA = create_post_data_scheme()

log_level = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}[config.get('log', 'log_level')]

logging.basicConfig(
    filename=config.get('log', 'log_file'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=log_level
)


@app.route('/fetch', methods=['POST'])
def collect_sensor_info():
    try:
        auth = UserAuth()
        username = request.authorization['username']
        password = request.authorization['password']

        logging.info('Received upload from: %s' % username)

        if not auth.authentificate(username, password):
            return Response(response='Wrong username/password',
                            status=httplib.UNAUTHORIZED)

        if not auth.authorize(ROLES):
            return Response(response='Not allowed for this user',
                            status=httplib.FORBIDDEN)

        logging.info('%s verified' % username)

        try:
            data = get_post_data(request.data, SCHEMA)

            db, collections, modules, start, end = map_keys(data)

            resolution = time_resolution(start, end, collections, modules)

            queries = create_query(db, collections, modules, to_database_key(start), to_database_key(end))

            results = get_database_info(queries)

            response = create_response(results, resolution)

        except ValueError as ve:
            return Response(str(ve), status=httplib.BAD_REQUEST)

        except TypeError as te:
            return Response(str(te), status=httplib.BAD_REQUEST)

        return Response(response=response, status=httplib.OK)

    except Exception as e:
        logging.error(str(e))

    return Response(response='', status=httplib.INTERNAL_SERVER_ERROR)


def get_post_data(post_data, scheme):
    try:
        data = json.loads(post_data)

    except ValueError:
        raise ValueError('Post data must be in json')

    if not validate(data=data, schema=scheme):
        raise ValueError('Wrong post data format')

    return data


def create_query(modules, start_time, end_time):
    queries = list()

    while start_time <= end_time:
        for m in modules:
            q = {
                ''
            }

            queries.append(q)

        start_time += datetime.timedelta(hours=1)

    return queries


def get_database_info(queries):
    results = list()
    # fatty...

    return results


def create_response(results, resolution):
    response = ''

    return response


if __name__ == '__main__':
    app.run()
