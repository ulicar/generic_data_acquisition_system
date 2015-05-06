#!/usr/bin/python

__author__ = 'jdomsic'

import logging
import json
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

        self.messages = list()
        self.current_core_id = None

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

    def on_message_received(self, message, message_type, properties, stop):
        if not (message_type == self.type or message_type == 'all'):
            self.consumer.reject_msg()

            return

        core_id = message['app_id']
        if self.current_core_id is not None and self.current_core_id != core_id:
            self.consumer.reject_msg()

            return

        if not self.validate(message):
            self.consumer.reject_msg()

            return

        # TODO: implement recieving bulk messages
        self.current_core_id = core_id
        self.messages.append(message)
        self.consumer.acknowledge_msg()
        if len(self.messages) >= 60:
            self.messages, module_messages = list(), self.divide_by_module()

            self.publisher.run_connection = True
            for module_type, msgs in module_messages.items():
                self.publisher.publish(module_messages, routing_key=module_type)

    def divide_by_module(self):
        msg_by_module = dict()
        for msg in self.messages:
            module_id = msg['module']
            if module_id not in msg_by_module:
                msg_by_module[module_id] = list()

            msg_by_module[module_id].append(msg)

        return msg_by_module

    def validate(self, message):
        try:
            validictory.validate(message, self.schema)

            return True

        except ValueError as ve:
            logging.warning(str(ve))
            logging.warning(str(message))

        return False


def main():
    args = argument_parser('Argument parser')
    cfg = Configuration().load_from_file(args.ini)

    logging.basicConfig(filename=cfg.log_file,
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=cfg.log_level)

    logging.info('Started Pigeon: %s. Collecting %s info.' % (cfg.app_id, cfg.type))
    message_selector = MessageSelector(cfg)
    message_selector.main()

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)
