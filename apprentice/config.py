__author__ = 'jdomsic'

import ConfigParser
import logging


class Configuration():
    def __init__(self):
        self.mq_url = None
        self.output_exchange = None
        self.routing_key = None

        self.log_file = None
        self.log_level = None

        self.app_id = None
        self.core_url = None
        self.token = None
        self.roles = None
        self.sleep_time = None

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
        self.output_exchange, self.routing_key = config.get('gdas', 'queue').split(':')
        self.app_id = config.get('gdas', 'app_id')

        self.core_url = config.get('apprentice', 'core_url')
        self.token = config.get('apprentice', 'password_token')
        self.sleep_time = config.get('apprentice', 'sleep_time')

        return self
