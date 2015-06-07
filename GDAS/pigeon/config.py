__author__ = 'jdomsic'

import ConfigParser
import logging

from message_scheme import create_core_scheme


class Configuration():
    def __init__(self):
        self.mq_url = None
        self.log_file = None
        self.output_exchange = None
        self.routing_key = None
        self.input_queue = None
        self.app_id = None
        self.type = None
        self.cores = None
        self.log_level = None
        self.schema = create_core_scheme()
        self.remapper_flag = None
        self.remapping = {}

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
        self.output_exchange = config.get('gdas', 'output_mq').split(':')[0]
        self.app_id = config.get('gdas', 'app_id')
        self.type = config.get('gdas', 'type')
        self.routing_key = config.get('pigeon', 'routing_key')
        self.cores = config.get('pigeon', 'cores')
        self.remapper_flag = config.getboolean('mapping', 'use_mapping')
        self.remapping = {
            'id': config.get('mapping', 'id'),
            'module': config.get('mapping', 'module'),
            'timestamp': config.get('mapping', 'timestamp'),
            'value': config.get('mapping', 'value')
        }

        return self
