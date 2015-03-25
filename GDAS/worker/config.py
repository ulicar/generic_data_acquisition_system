__author__ = 'jdomsic'

import ConfigParser
import logging

from logging.handlers import TimedRotatingFileHandler


class Configuration():
    def __init__(self):
        pass

    def load_from_file(self, filename):
        config = ConfigParser.ConfigParser()
        config.read(filename)

        self.mq_url = config.get('core', 'mq_url')
        self.queue_name = config.get('core', 'queue')
        self.database = config.get('core', 'database').split(':')
        self.collection_name = config.get('core', 'collection').split(':')
        self.log_file = config.get('log', 'log_file')

        return self


class Logger():
    logger = None
    log_filename = None

    def create_logger(self, filename):
        config = ConfigParser.ConfigParser()
        config.read(filename)

        self.log_filename = config.get('log', 'log_file')

        log_handler = TimedRotatingFileHandler(self.log_filename)
        log_handler.setLevel(logging.WARNING)

        return log_handler
