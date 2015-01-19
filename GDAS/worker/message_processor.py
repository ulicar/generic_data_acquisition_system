__author__ = 'jdomsic'

import sys
import pika
from config import Configuration

from utils.input.argument_parser import get_arguments


def main():
    args = get_arguments()
    ini_file = args.ini

    try:
        cfg = Configuration.load_from_file(ini_file)

        mq, mq_channel = open_mq_channel(cfg.msg_queue_url, 'weather_data')
        print ' [*] Waiting for messages. To exit press CTRL+C'


        mq_channel.basic_consume(process_message,
                              queue='hello',
                              no_ack=True)

        mq_channel.start_consuming()

    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)


def open_mq_channel(mq_url, channel_name):
    mq = pika.BlockingConnection(pika.ConnectionParameters(host=mq_url))
    mq_channel = mq.channel()
    mq_channel.queue_declare(queue=channel_name)
    return mq, mq_channel

def process_message(ch, method, properties, body):


if __name__ == '__main__':
    main()