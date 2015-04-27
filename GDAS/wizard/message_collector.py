__author__ = 'jdomsic'

import ConfigParser
import httplib
import json
import logging
import sys

from flask import Flask
from flask import Response
from flask import request

from GDAS.utils.security import UserAuth
from GDAS.utils.communication import publisher

app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

QUEUE = config.get('gdas', 'queue')
NAME = config.get('gdas', 'name')
MQ_URL = config.get('gdas', 'mq_url')
DATABASE = config.get('gdas', 'database').split(':')

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


def validate_data(user_data, config):
    scheme = config['DATA_SCHEME']
    for data in user_data:
        if not validictory.validate(data, scheme):
            return False

    return True


def publish_to_mq(messages, config):
    assert isinstance(messages, list), "messages must be a list"

    exchange_name, queue_name = QUEUE.split(':')
    routing_key = get_message_type(messages[0], config)

    settings = publisher.Settings(NAME, queue_name, exchange_name, routing_key)

    queue = publisher.Publisher(settings)

    queue.publish(messages)


def get_message_type(user_data, config):
    return json.loads(user_data)[0][config['DATA_SCHEME_KEY']]


@app.route('/wizard/upload', methods=['POST'])
def collect_sensor_info():
    auth = UserAuth()

    if not auth.authentificate(request.authorization):
        return Response(response='Wrong username/password',
                        status=httplib.UNAUTHORIZED)

    if not auth.authorize(app, request.authorization):
        return Response(response='Not allowed for this user',
                        status=httplib.FORBIDDEN)

    logging.info('Received upload from: %s' % request.authorization.username)

    publish_to_mq([request.data], app.config)

    return Response(response='uploaded', status=httplib.OK)


if __name__ == '__main__':
    app.run()
