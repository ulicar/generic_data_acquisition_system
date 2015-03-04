__author__ = 'jdomsic'

import sys
import pika
import json

from config import Configuration
from pymongo import Connection

from util.input.argument_parser import argument_parser
from util.communication.consumer import Consumer
from util.communication.consumer import Settings


class MessageProcessor(object):
    def __init__(self, cfg):
        self.db = cfg.database
        self.mq = cfg.mq_url
        self.queue_name = cfg.queue
        self.loq = cfg.log_file

    def main(self):
        settings = Settings('amqp://guest:guest@localhost:5672/%2F',
                'example-queue'
        )

        consumer = Consumer(settings)

        def callback(message, message_type, properties):
            print str(message)
            # OPTIONAL 1: consumer.acknowledge_msg()
            # OPTIONAL 2: consumer.reject_msg()

        consumer.consume(callback)

    def open_mq_channel(self, mq_url):
        mq = pika.BlockingConnection(pika.ConnectionParameters(host=mq_url))
        mq_channel = mq.channel()
        return mq, mq_channel


    def process_message(self, ch, method, properties, body):
        save_to_database(body, Connection('localhost', 27017), 'sensor_data', 'weather_data')


    def save_to_database(self, message, client, db_name, db_collection):
        database = client[db_name]
        collection = database[db_collection]
        msg = json.loads(message)
        collection.insert(msg)


def main():
    args = argument_parser('GDAS data processor')
    cfg = Configuration().load_from_file(args.ini)

    message_processor = MessageProcessor(cfg)

    mq, mq_channel = open_mq_channel(cfg.mq_url)
    mq_channel.basic_consume(process_message, queue=cfg.msg_queue, no_ack=True)
    mq_channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)