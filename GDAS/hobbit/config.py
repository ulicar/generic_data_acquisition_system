__author__ = 'jdomsic'

import ConfigParser
import logging


class Configuration():
    def __init__(self):
        self.mq_url = None
        self.output_exchange = None
        self.core_url = None
        self.logger = None
        self.name = None

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

        self.logger = logging.basicConfig(
            filename=config.get('log', 'log_file'),
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=log_level
        )

        self.mq_url = config.get('GDAS', 'mq_url')
        self.output_exchange = config.get('GDAS', 'output_mq')
        self.name = config.get('GDAS', 'name')

        return self
