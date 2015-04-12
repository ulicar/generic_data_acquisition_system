__author__ = 'jdomsic'

import ConfigParser
import logging


class Configuration():
    def __init__(self):
        self.mq_url = None
        self.queue_name = None
        self.database = None
        self.collection_name = None
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
        }[config.get('log','log_level']

        self.mq_url = config.get('gdas', 'mq_url')
        self.queue_name = config.get('gdas', 'queue')
        self.database = config.get('gdas', 'database').split(':')
        self.collection_name = config.get('gdas', 'collection')
        self.logger = logging.basicConfig(
                filename=config.get('log', 'log_file'),
                filemode='a',
                format='%(asctime)s - %(levelname)s - %(message)s'
                level=log_level
        )
        self.name = config.get('gdas', 'name')

        return self

