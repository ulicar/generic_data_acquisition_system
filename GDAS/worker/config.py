__author__ = 'jdomsic'

import ConfigParser
import logging


class Configuration():
    def __init__(self):
        self.mq_url = None
        self.queue_name = None
        self.database = None
        self.collection = None
        self.app_id = None

        self.log_level = None
        self.log_file = None

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
        self.queue_name = config.get('gdas', 'queue')
        self.database = config.get('gdas', 'database').split(':')
        self.collection = config.get('gdas', 'collection').split(':')
        self.app_id = config.get('gdas', 'app_id')

        return self

