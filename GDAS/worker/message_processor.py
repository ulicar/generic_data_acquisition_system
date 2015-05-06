#!/usr/bin/python

__author__ = 'jdomsic'

import datetime
import json
import logging
import sys

from config import Configuration
from GDAS.utils.database.connection import Fatty
from GDAS.utils.input.argument_parser import argument_parser
from GDAS.utils.communication.consumer import Consumer
from GDAS.utils.communication.consumer import Settings


class MessageProcessor(object):
    def __init__(self, cfg):
        self.db = Fatty(cfg.database)
        self.db.open(cfg.collection[0], cfg.collection[1])

        self.mq = cfg.mq_url
        self.queue_name = cfg.queue

        self.consumer = None
        self.type = cfg.type
        self.core_id = cfg.core_id

        self.messages = list()

    def main(self):
        settings = Settings(self.mq, self.queue_name)
        self.consumer = Consumer(settings)
        self.consumer.consume(self.process_message)

    def process_message(self, messages, message_type, properties, stop):
        messages = json.loads(messages)
        for msg in messages:
            if msg['app_id'] != self.core_id or msg['module'] != self.type:
                self.consumer.reject_msg()

                return
        try:
            self.messages.append(messages)
            self.consumer.acknowledge_msg()
            if len(self.messages) >= 10:
                self.save()
                self.messages = list()

        except Exception as e:
            logging.error(str(e))
            logging.info(str(self.messages))
            raise Exception

    def save(self):
        self.messages, data = list(), self.prepare_data()
        for module, hours in data.items():
            for hour, measurements in hours.items():
                db_key = {
                    'module': module,
                    'time': hour
                }

                self.update_record(db_key, measurements)

    def prepare_data(self):
        """
            data = {
                'module': {
                    'time': {mesuerements}
                    }
                }

        """
        data = dict()
        for msgs in self.messages:
            for msg in msgs:
                module = msg['module']
                if module not in data:
                    data[module] = {}

                sensor_time_data = datetime.datetime.fromtimestamp(int(msg['timestamp']))
                sensor_time = sensor_time_data.minute * 60 + sensor_time_data.second
                sensor_value = msg['value']
                measurement = {'TIMESTAMP.%d' % sensor_time: sensor_value}

                time = sensor_time_data.strftime('%Y-%m-%d-%H')
                if time not in data[module]:
                    data[module][time] = {}

                data[module][time].update(measurement)

        return data

    def update_record(self, keys, time_series_data):
        self.db.append(keys, time_series_data)

        return


def main():
    args = argument_parser('Argument parser')
    cfg = Configuration().load_from_file(args.ini)

    logging.basicConfig(filename=cfg.log_file,
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=cfg.log_level)

    logging.info('Started Worker: %s. Saving %s info.' % (cfg.app_id, cfg.type))

    message_processor = MessageProcessor(cfg)
    message_processor.main()

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)
