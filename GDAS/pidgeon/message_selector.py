__author__ = 'jdomsic'

import sys
import json

import pika

from config import Configuration
from util.input.argument_parser import configuration_parser


def main():
    args = configuration_parser('Data Collector parser')
    cfg = Configuration().load_from_file(args.ini)

    input_mq, input_mq_channel = open_mq_channel(cfg.mq_url)
    output_mq, output_mq_channel = open_mq_channel(cfg.mq_url)

    input_mq_channel.basic_consume(on_msg_received, queue='master', no_ack=True)
    input_mq_channel.start_consuming()

    output_mq.close()
    input_mq.close()


def open_mq_channel(mq_url):
    mq = pika.BlockingConnection(pika.ConnectionParameters(host=mq_url))
    mq_channel = mq.channel()
    return mq, mq_channel


def on_msg_received(ch, method, properties, body):
    send_to_mq(json.dumps(json.loads(body)), ch, 'weather_collection', '')


def send_to_mq(msg, channel, exchange, routing_key):
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)
