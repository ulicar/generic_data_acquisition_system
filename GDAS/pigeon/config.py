__author__ = 'jdomsic'

import ConfigParser
import logging

from message_scheme import create_message_scheme


class Configuration():
    def __init__(self):
        self.mq_url = None
        self.log_file = None
        self.output_exchange = None
        self.routing_key = None
        self.input_queue = None
        self.app_id = None
        self.type = None
        self.log_level = None
        self.schema = create_message_scheme()

    def load_from_file(self, filename):
        config = ConfigParser.ConfigParser()
        config.read(filename)

        self.log_level = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }[config.get('log', 'log_level')]
        self.log_file = config.get('log', 'log_file')

        self.mq_url = config.get('gdas', 'mq_url')
        self.input_queue = config.get('gdas', 'input_mq').split(':')[1]
        self.output_exchange, self.routing_key = config.get('gdas', 'output_mq').split(':')
        self.app_id = config.get('gdas', 'app_id')
        self.type = config.get('gdas', 'type')

        return self
