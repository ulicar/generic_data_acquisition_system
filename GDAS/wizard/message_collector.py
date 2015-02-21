__author__ = 'jdomsic'

import httplib
import json

import pika
from flask import Flask
from flask import Response
from flask import request

from util.auth.auth import Auth
from utils.auth.authentication import authentificate
from utils.auth.authorization import authorize


app = Flask(__name__)
app.config.from_object('config.ProductionConfig')


def get_received_data(raw_data):
    return json.loads(raw_data)


def check_format(raw_data):
    try:
        return json.loads(raw_data)
    except ValueError:
        return None


def open_mq_channel(mq_url):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=mq_url))
    channel = conn.channel()
    return conn, channel


def send_to_mq(msg, channel, exchange, routing_key=''):
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)

@app.route('/wizard/upload', methods=['POST'])
def collect_sensor_info():
    with open(app.config['LOG'], 'r') as l:
        db = app.config['DATABASE']
        auth = Auth(request)
        if not authentificate(auth.username, auth.password, db):
            return Response(response='', status=httplib.UNAUTHORIZED)

        required_roles = app.config['ROLES']
        if not authorize(auth.username, required_roles, db):
            return Response(response='', status=httplib.FORBIDDEN)

        is_required_format = check_format(request.data)
        if not is_required_format:
            Response(response='Not in JSON', status=httplib.BAD_REQUEST)


        mq, mq_channel = open_mq_channel(app.cfg.msg_queue_url)
        data = get_received_data(request.data)
        for msg in data:
            send_to_mq(json.dumps(msg), mq_channel, app.cfg.exchange, '')
        mq.close()

        return Response(response='RESPONSE', status=httplib.OK)

    return Response(response='error', status=httplib.INTERNAL_SERVER_ERROR)


if __name__ == '__main__':
    app.run()
