__author__ = 'jdomsic'

import sys
import ConfigParser
import pika

from config import Configuration

from utils.input.argument_parser import get_arguments


def main():
    args = get_arguments()
    ini_file = args.ini

    try:
        cfg = Configuration().load_from_file(ini_file)

        input_mq, input_mq_channel = open_mq_channel(cfg.msg_queue_url, 'requests')
        mq_exchange, mq_routing_key = '', ''
        sent_to_mq(input_mq_channel, mq_exchange, mq_routing_key, 'Hello World!')
        input_mq.close()

    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)


def open_mq_channel(mq_url, channel_name):
    mq = pika.BlockingConnection(pika.ConnectionParameters(host=mq_url))
    mq_channel = mq.channel()
    mq_channel.queue_declare(queue=channel_name)
    return mq, mq_channel


def sent_to_mq(channel, exchange, routing_key, msg):
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)


if __name__ == '__main__':
    main()