#!/usr/bin/python

__author__ = 'jdomsic'

import logging
import sys

from config import Configuration
from GDAS.utils.database.connection import Fatty
from GDAS.utils.input.argument_parser import argument_parser
from GDAS.utils.communication.consumer import Consumer
from GDAS.utils.communication.consumer import Settings


class MessageProcessor(object):
    def __init__(self, cfg):
        self.db = Fatty(cfg.database)
        self.db.open(cfg.collection[0], cfg.collection[1])

        self.mq = cfg.mq_url
        self.queue_name = cfg.queue
        self.consumer = None

    def main(self):
        settings = Settings(self.mq, self.queue_name)
        self.consumer = Consumer(settings)
        self.consumer.consume(self.process_message)

    def process_message(self, message, message_type, properties):
        print str(message)

        self.consumer.acknowledge_msg()
        self.save_to_database(message)

    def save_to_database(self, message):
        self.db.write(message)


def main():
    args = argument_parser('Argument parser')
    cfg = Configuration().load_from_file(args.ini)

    logging.basicConfig(filename=cfg.log_file,
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=cfg.log_level)

    logging.info('Started Worker: %s. Saving %s info.' % (cfg.app_id, cfg.type))

    message_processor = MessageProcessor(cfg)
    message_processor.main()

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)
