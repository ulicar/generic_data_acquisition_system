__author__ = 'jdomsic'

import ConfigParser
import logging


class Configuration():
    def __init__(self):
        self.database = None
        self.mq_url = None
        self.log_file = None
        self.output_exchange = None
        self.input_exchange = None
        self.name = None
        self.logger = None

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

        self.mq_url = config.get('gdas', 'mq_url')
        self.input_exchange = config.get('gdas', 'input_mq')
        self.output_exchange = config.get('gdas', 'output_mq')
        self.database = config.get('gdas', 'database').split(':')

        self.logger = logging.basicConfig(
            filename=config.get('log', 'log_file'),
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=log_level
        )
        self.name = config.get('GDAS', 'name')

        return self
