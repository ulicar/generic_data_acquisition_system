__author__ = 'jdomsic'

import ConfigParser
import logging

from flask import Flask


class Config(object):
    def __init__(self):
        self.DEBUG = False
        self.TESTING = False

        self.MQ_URL = None
        self.QUEUE = None
        self.LOGGER = None
        self.NAME = None

        self.DATA_SCHEME_KEY = 'module'
        self.DATA_SCHEME = {
        'TYPE': ''
    }

    def load_from_file(self, filename):
        config = ConfigParser.ConfigParser()
        config.read(filename)
        log_level = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }[config.get('log', 'log_level')]

        self.MQ_URL = config.get('gdas', 'mq_url')
        self.QUEUE = config.get('gdas', 'queue')

        self.LOGGER = logging.basicConfig(
            filename=config.get('log', 'log_file'),
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=log_level
        )
        self.NAME = config.get('gdas', 'name')


app = Flask(__name__)
config = Config()
config.load_from_file()
app.config.from_object(config)

