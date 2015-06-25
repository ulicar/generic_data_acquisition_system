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
from GDAS.utils.database.connection import Fatty

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


@app.route('/fetch', methods=['GET', 'POST'])
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
            data = collect_request_data(request, request.method, SCHEMA)

            db, collections, modules, start, end = map_keys(data)

            #resolution = time_resolution(start, end, int(collections), int(modules))

            queries = create_query(modules, start_time=start, end_time=end)

            results = get_database_info(db, collections, queries)

            response = create_response(results)  # resolution

        except ValueError as ve:
            return Response(str(ve), status=httplib.BAD_REQUEST)

        except TypeError as te:
            return Response(str(te), status=httplib.BAD_REQUEST)

        return Response(response=response, status=httplib.OK)

    except Exception as e:
        logging.error(str(e))

    return Response(response='', status=httplib.INTERNAL_SERVER_ERROR)


def collect_request_data(request_data, method, scheme):
    try:
        if method == 'POST':
            data = collect_post_data(request_data.data)
        else:
            data = collect_get_data(request_data.args)

    except ValueError:
        raise ValueError('Post data must be in json')

    # Raises Exception on error
    validate(data=data, schema=scheme)

    return data


def collect_post_data(post_data):

    return json.loads(post_data)


def collect_get_data(query_args):
    data = {
        'user': query_args['user'],
        'modules': query_args.getlist('modules'),
        'core': query_args['core'],
        'time': {
            'from': query_args['from'],
            'to': query_args['to']
            }
    }

    return data

def create_query(modules, start_time, end_time):
    queries = list()
    while start_time <= end_time:
        for m in modules:
            q = {
                'module': m,
                'time': to_database_key(start_time)
            }

            queries.append(q)

        start_time += datetime.timedelta(hours=1)

    return queries


def get_database_info(db, collection, queries):
    fatty = Fatty()
    fatty.open(db, collection)
    results = list()
    for q in queries:
        data = fatty.get_record(q)

        if data:
            results.append({
                'module': data['module'],
                'time': data['time'],
                'measurements': data['data']
            })

    return results


def create_response(results, resolution=None):
    response = json.dumps(results, indent=4)

    return response


if __name__ == '__main__':
    app.run()
