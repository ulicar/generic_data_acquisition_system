__author__ = 'jdomsic'

import sys

from util.communication import consumer
from util.communication import publisher
from util.input.argument_parser import argument_parser
from config import Configuration


class MessageSelector(object):
    def __init__(self, cfg):
        self.app_id = cfg.app_id
        self.mq_url = cfg.mq_url
        self.input = cfg.input
        self.output = cfg.output
        self.loq = cfg.log_file
        self.routing_key = cfg.routing_key
        self.consumer = None
        self.publisher = None

    def process(self, message):
        # TODO: list -> to str maybe
        return message

    def on_message_received(self, message, message_type, properties):
        print str(message)

        self.publisher.publish(self.process(message))
        self.consumer.acknowledge_msg()

    def main(self):
        publisher_settings = publisher.Settings(
            self.app_id,
            self.mq_url,
            self.output,
            self.routing_key
        )
        self.publisher = publisher.Publisher(publisher_settings)

        consumer_settings = consumer.Settings(self.mq_url, self.input)
        self.consumer = consumer.Consumer(consumer_settings)
        self.consumer.consume(self.on_message_received)


def main():
    args = argument_parser('Data Collector parser')
    cfg = Configuration().load_from_file(args.ini)

    message_selector = MessageSelector(cfg)
    message_selector.main()

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)
