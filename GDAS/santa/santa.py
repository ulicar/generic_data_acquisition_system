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
            schema = crete_post_data_scheme()

            data = get_post_data(request.data, schema)

            db, collections, modules, start, end = map_keys(schema, data)

            resolution = time_resolution(start, end, collections, modules)

            queries = create_query(start, end)

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


def create_query(keys):
    queries = list()

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
