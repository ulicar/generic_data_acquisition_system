#!/usr/bin/python

__author__ = 'jdomsic'

import logging
import sys
import validictory

from GDAS.utils.communication import consumer
from GDAS.utils.communication import publisher
from GDAS.utils.input.argument_parser import argument_parser
from config import Configuration


class MessageSelector(object):
    def __init__(self, cfg):
        self.app_id = cfg.app_id
        self.mq_url = cfg.mq_url
        self.input = cfg.input_queue
        self.output = cfg.output_exchange
        self.loq = cfg.log_file
        self.routing_key = cfg.routing_key
        self.type = cfg.type
        self.schema = cfg.schema

        self.consumer = None
        self.publisher = None

    def main(self):
        publisher_settings = publisher.Settings(
            self.app_id,
            self.mq_url,
            self.output,
            self.routing_key
        )
        self.publisher = publisher.Publisher(publisher_settings)

        consumer_settings = consumer.Settings(self.mq_url, self.input)
        self.consumer = consumer.Consumer(consumer_settings)

        self.consumer.consume(self.on_message_received)

    def on_message_received(self, message, message_type, properties):
        if message_type != self.type:
            self.consumer.reject_msg()

        if not self.validate(message):
            # TODO: what to do with them
            self.consumer.reject_msg()

            return

        # TODO: implement recieving bulk messages

        self.publisher.publish(message)
        self.consumer.acknowledge_msg()

    def validate(self, message):
        try:
            return validictory.validate(message, self.schema)

        except ValueError as ve:
            logging.WARNING(str(ve))
            logging.WARNING(str(message))

        return False


def main():
    args = argument_parser('Data Collector parser')
    cfg = Configuration().load_from_file(args.ini)

    logging.basicConfig(filename=cfg.log_file,
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=cfg.log_level)

    logging.INFO('Started Pigeon: %s. Collecting %s' % (cfg.name, cfg.type))
    message_selector = MessageSelector(cfg)
    message_selector.main()

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)
