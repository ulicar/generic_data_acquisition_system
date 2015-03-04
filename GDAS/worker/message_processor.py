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
        settings = Settings(self.mq, self.queue_name)
        consumer = Consumer(settings)
        consumer.consume(self.process_message)


    def process_message(self, message, message_type, properties):
            print str(message)
            # OPTIONAL 1: consumer.acknowledge_msg()
            # OPTIONAL 2: consumer.reject_msg()
            self.save_to_database()

    """
    def process_message(self, ch, method, properties, body):
        save_to_database(body, Connection('localhost', 27017), 'sensor_data', 'weather_data')
    """

    def save_to_database(self, message, client, db_name, db_collection):
        database = client[db_name]
        collection = database[db_collection]
        msg = json.loads(message)
        collection.insert(msg)


def main():
    args = argument_parser('GDAS data processor')
    cfg = Configuration().load_from_file(args.ini)

    message_processor = MessageProcessor(cfg)
    message_processor.main()

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)