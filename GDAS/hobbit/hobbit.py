#!/usr/bin/python

__author__ = 'jdomsic'

import logging
import requests
import sys
import time

from GDAS.utils.input.argument_parser import argument_parser
from GDAS.utils.communication import publisher
from config import Configuration


class Hobbit(object):
    def __init__(self, cfg):
        self.app_id = cfg.app_id
        self.core_url = cfg.core_url
        self.communication_token = cfg.token
        self.sleep_time = int(cfg.sleep_time)

        self.mq_url = cfg.mq_url
        self.exchange = cfg.output_exchange
        self.routing_key = cfg.routing_key

        self.publisher = None

    def main(self):
        publisher_settings = publisher.Settings(
            app_id=self.app_id,
            mq_url=self.mq_url,
            exchange=self.exchange,
            routing_key=self.routing_key
        )
        self.publisher = publisher.Publisher(publisher_settings)

        while True:
            messages = self.get_messages()

            self.publish_to_mq(messages)

    def get_messages(self):
        return requests.get(
            url=self.core_url,
            headers={'token': self.communication_token},
            verify=False
        ).json()

    def publish_to_mq(self, messages):
        if not isinstance(messages, list):
            raise TypeError

        self.publisher.run_connection = True
        self.publisher.publish(messages)

        time.sleep(self.sleep_time)

if __name__ == '__main__':
    try:
        args = argument_parser('Data requester argument parser')
        cfg = Configuration().load_from_file(args.ini)

        logging.basicConfig(
            filename=cfg.log_file,
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=cfg.log_level
        )

        hobbit = Hobbit(cfg)
        logging.info('Starting hobit %s. Collecting from %s' % (
            hobbit.app_id,
            hobbit.core_url
        ))

        hobbit.main()

    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(-1)

    sys.exit(0)
