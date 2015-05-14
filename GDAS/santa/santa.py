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

from schema import *
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


def get_post_data(data, scheme):
    pass

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

            keys = map_keys(schema, data)

            query = create_query(keys)

            results = get_database_info(query)

            response = create_response(results, resolution)

            return Response(response, status=httplib.OK)

        except ValueError as ve:
            return Response(str(ve), status=httplib.BAD_REQUEST)

        except TypeError as te:
            return Response(str(te), status=httplib.BAD_REQUEST)

        return Response(response='uploaded', status=httplib.OK)

    except Exception as e:
        logging.error(str(e))

    return Response(response='', status=httplib.INTERNAL_SERVER_ERROR)


if __name__ == '__main__':
    app.run()
