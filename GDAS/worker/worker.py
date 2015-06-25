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


class Worker(object):
    def __init__(self, cfg):
        self.distdb = Fatty(cfg.database)
        self.db = cfg.db

        self.mq = cfg.mq_url
        self.queue_name = cfg.queue

        self.consumer = None
        self.cores = cfg.cores
        self.current_core_id = None
        self.messages = list()

    def main(self):
        settings = Settings(self.mq, self.queue_name)
        self.consumer = Consumer(settings)
        self.consumer.consume(self.process_message)

    def process_message(self, message, _message_type, _properties, _stop):
        msg = json.loads(message)
        core_id = msg['core']
        data = msg['data']

        if core_id not in self.cores:
            self.consumer.reject_msg()

            return

        if self.current_core_id is not None and self.current_core_id != core_id:
            self.consumer.reject_msg()

            return

        self.current_core_id = core_id
        try:
            self.messages.extend(data)
            self.consumer.acknowledge_msg()
            if len(self.messages) < 10:
                return

            self.save()
            self.messages = list()
            self.current_core_id = None

        except Exception as err:
            logging.error(str(err))
            logging.info(str(self.messages))
            raise Exception

    def save(self):
        data = self.prepare_data()
        for (module, time), value in data.items():
            db_key = {
                'module': module,
                'time': time
            }
            measurements = value['values']
            self.update_record(db_key, measurements)

    def prepare_data(self):
        """
            all_data = [
                (<module>, <time>) : {
                    'module': <module>,
                    'time': <time>
                    'values': {
                        data.<sec> :<measurement>,
                        ...,
                },
                ...
            ]

        """
        all_data = {}
        for msg in self.messages:
            dt = datetime.datetime.fromtimestamp(int(msg['timestamp']))
            time_value = dt.strftime('%Y-%m-%d-%H')

            if (msg['id'], time_value) not in all_data:
                hourly_measurement = dict(
                    {
                        'module': msg['id'],
                        'time': time_value,
                        'values': {}
                    }
                )
                all_data[(msg['id'], time_value)] = hourly_measurement

            else:
                hourly_measurement = all_data[(msg['id'], time_value)]

            hourly_measurement['values']['%s.%s' % ('data', str(dt.minute * 60 + dt.second))] \
                = json.dumps(msg['value'])

        return all_data

    def update_record(self, keys, time_series_data):
        self.distdb.open(self.db, self.current_core_id)
        self.distdb.append(keys, time_series_data)

        return


def main():
    args = argument_parser('Argument parser')
    cfg = Configuration().load_from_file(args.ini)

    logging.basicConfig(filename=cfg.log_file,
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=cfg.log_level)

    logging.info('Started Worker: %s. Saving %s info.' % (cfg.app_id, cfg.db))

    worker = Worker(cfg)
    worker.main()

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)
