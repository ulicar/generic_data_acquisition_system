__author__ = 'jdomsic'

import ConfigParser
import logging


class Configuration():
    def __init__(self):
        self.log_level = None
        self.log_file = None

        self.mq_url = None
        self.database = None

        self.queue_name = None
        self.collection = None
        self.app_id = None
        self.type = None
        self.core_id = None

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
        self.log_file = config.get('gdas', 'log_file')

        self.mq_url = config.get('gdas', 'mq_url')
        self.database = config.get('gdas', 'database').split(':')

        self.collection = config.get('worker', 'collection').split(':')
        self.app_id = config.get('worker', 'app_id')
        self.queue_name = config.get('worker', 'queue')
        self.type = config.get('worker', 'type')
        self.core_id = config.get('worker', 'core_id')

        return self

