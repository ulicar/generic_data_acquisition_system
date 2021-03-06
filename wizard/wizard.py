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

from GDAS.utils.security.auth import UserAuth
from GDAS.utils.communication import publisher


app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

QUEUE = config.get('gdas', 'queue')
NAME = config.get('gdas', 'name')
MQ_URL = config.get('gdas', 'mq_url')
ROLES = config.get('wizard', 'required_roles').split(',')

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


def publish_to_mq(core_data):
    if not isinstance(core_data, list):
        raise TypeError

    exchange_name, queue_name = QUEUE.split(':')
    routing_key = queue_name.split('.')[-1]
    settings = publisher.Settings(
        app_id=NAME,
        mq_url=MQ_URL,
        exchange=exchange_name,
        routing_key=routing_key
    )

    queue = publisher.Publisher(settings)
    queue.publish(core_data)


@app.route('/upload', methods=['POST'])
def collect_sensor_info():
    try:
        auth = UserAuth()
        username = request.authorization['username']
        password = request.authorization['password']

        if not auth.authentificate(username, password):
            return Response(response='Wrong username/password',
                            status=httplib.UNAUTHORIZED)

        if not auth.authorize(ROLES):
            return Response(response='Not allowed for this user',
                            status=httplib.FORBIDDEN)

        logging.info('Received upload from: %s' % username)

        try:
            publish_to_mq(json.loads(request.data))

        except StopIteration:
            return Response('Empty payload', status=httplib.BAD_REQUEST)

        except ValueError:
            return Response('Not in JSON', status=httplib.BAD_REQUEST)

        except TypeError:
            return Response('Payload must be a list of messages', status=httplib.BAD_REQUEST)

        return Response(response='uploaded', status=httplib.OK)

    except Exception as e:
        logging.error(str(e))

    return Response(response='', status=httplib.INTERNAL_SERVER_ERROR)


if __name__ == '__main__':
    app.run()
