__author__ = 'jdomsic'

import ConfigParser
import logging

from logging.handlers import TimedRotatingFileHandler

class Configuration():
    database = None
    msg_queue_url = None
    log_file = None

    def load_from_file(self, filename):
        config = ConfigParser.ConfigParser()
        config.read(filename)

        self.msg_queue_url = config.get('core', 'message_queue')
        self.exchange = config.get('core', 'exchange')
        self.database = config.get('core', 'database').split(':')
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
