__author__ = 'jdomsic'

import ConfigParser
import logging


class Configuration():
    def __init__(self):
        self.database = None
        self.mq_url = None
        self.log_file = None
        self.output_exchange = None
        self.routing_key = None
        self.input_queue = None
        self.name = None
        self.type = None
        self.log_level = None

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

        self.mq_url = config.get('gdas', 'mq_url')
        self.input_queue = config.get('gdas', 'input_mq').split(':')[1]
        self.output_exchange, self.routing_key = config.get('gdas', 'output_mq').split(':')
        self.database = config.get('gdas', 'database').split(':')
        self.name = config.get('GDAS', 'name')

        return self
