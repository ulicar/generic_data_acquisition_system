__author__ = 'jdomsic'

import ConfigParser
import logging


class Configuration():
    def __init__(self):
        self.log_level = None
        self.log_file = None

        self.mq_url = None
        self.database = None

        self.queue = None
        self.db = None
        self.app_id = None
        self.cores = None

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
        self.database = config.get('gdas', 'database').split(':')
        self.queue = config.get('gdas', 'queue')

        self.db = config.get('worker', 'db')
        self.app_id = config.get('worker', 'app_id')

        self.cores = config.get('worker', 'cores').strip().split(':')

        return self
