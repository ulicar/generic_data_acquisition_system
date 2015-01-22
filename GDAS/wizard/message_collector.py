__author__ = 'jdomsic'

import httplib
import json
import pika

from flask import Response
from flask import request

from initialize import app
from utils.auth.auth import Auth
from utils.auth.authentication import authentificate
from utils.auth.authorization import authorize
from utils.database.connection import get_db_connection

@app.route('/wizard/upload', methods=['POST'])
def collect_sensor_info():
    with open(app.cfg.log_file, 'r') as l:

        db = get_db_connection()
        auth = Auth(request)
        if not authentificate(auth.username, auth.password, db):
            return Response(response='', status=httplib.UNAUTHORIZED)

        required_roles = app.cfg.required_roles
        if not authorize(auth.username, required_roles, db):
            return Response(response='', status=httplib.FORBIDDEN)

        is_required_format = check_format(request.data)
        if not is_required_format:
            Response(response='Not in JSON', status=httplib.BAD_REQUEST)

        mq, mq_channel = open_mq_channel(app.cfg.msg_queue_url)

        data = get_received_data(request.data)
        for msg in data:
            send_to_mq(msg, mq_channel, app.cfg.exchange, '')
        mq.close()

        return Response(response='RESPONSE', status=httplib.OK)

    return Response(response='error', status=httplib.INTERNAL_SERVER_ERROR)


def get_received_data(raw_data):
    data = []

    # rework
    for entry in raw_data:
        data.append(entry)

    return data


def check_format(raw_data):
    try:
        return json.loads(raw_data)
    except Exception:
        return None


def save_to_database(message, db, db_collection):
    collection = db[db_collection]
    collection.insert(str(message))


def open_mq_channel(mq_url):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=mq_url))
    channel = conn.connect()
    return conn, channel


def send_to_mq(msg, channel, exchange, routing_key=''):
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)


if __name__ == '__main__':
    app.run()
