__author__ = 'jdomsic'

import sys
import pika
import json

from config import Configuration
from pymongo import Connection

from util.input.argument_parser import get_arguments


def main():
    args = get_arguments()
    ini_file = args.ini

    try:
        cfg = Configuration().load_from_file(ini_file)

        mq, mq_channel = open_mq_channel(cfg.mq_url)
        mq_channel.basic_consume(process_message, queue=cfg.msg_queue, no_ack=True)
        mq_channel.start_consuming()

    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)


def open_mq_channel(mq_url):
    mq = pika.BlockingConnection(pika.ConnectionParameters(host=mq_url))
    mq_channel = mq.channel()
    return mq, mq_channel


def process_message(ch, method, properties, body):
    save_to_database(body, Connection('localhost', 27017), 'sensor_data', 'weather_data')


def save_to_database(message, client, db_name, db_collection):
    database = client[db_name]
    collection = database[db_collection]
    msg = json.loads(message)
    collection.insert(msg)


if __name__ == '__main__':
    main()