__author__ = 'jdomsic'

import httplib
import json
import validictory

from configuration import app
from flask import Response
from flask import request

from util.database.connection import connect_to_db
from util.security import auth

from util.communication import publisher


def validate_data(user_data, app):
    scheme = app.config['DATA_SCHEME']
    for data in user_data:
        if not validictory.validate(data, scheme):
            return False

    return True


def publish_to_mq(messages, app):
    assert isinstance(messages, list), "messages must be a list"

    routing_key = get_message_type(messages[0], app)

    settings = publisher.Settings(app.config['APP_ID'],
                                  app.config['MQ_URL'],
                                  app.config['EXCHANGE'],
                                  routing_key)

    queue = publisher.Publisher(settings)
    queue.publish(messages)


def get_message_type(user_data, app):
    return json.loads(user_data)[0][app.config['DATA_SCHEME_KEY']]


@auth.requires_auth
@app.route('/wizard/upload', methods=['POST'])
def collect_sensor_info():
    with open(app.config['LOG'], 'r') as l:
        db_connection = connect_to_db(app)
        if not auth.authentificate(request, db_connection):
            return Response(response='Wrong username/password',
                            status=httplib.UNAUTHORIZED)

        if not auth.authorize(app, request, db_connection):
            return Response(response='Not allowed for this user',
                            status=httplib.FORBIDDEN)

        if not validate_data(request.data, app):
            Response(response='Data not in json', status=httplib.BAD_REQUEST)

        messages = [request.data]
        publish_to_mq(messages, app)

        return Response(response='RESPONSE', status=httplib.OK)

    return Response(response='error', status=httplib.INTERNAL_SERVER_ERROR)


if __name__ == '__main__':
    app.run()
