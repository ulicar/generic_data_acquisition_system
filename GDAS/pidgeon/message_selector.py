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
        config = ConfigParser.ConfigParser()
        config.read(ini_file)

        cfg = Configuration().load_from_file(ini_file)

        mq = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.msg_queue_url))
        mq_channel = mq.channel()
        mq_channel.queue_declare(queue='hello')
        mq_channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

        print " [x] Sent 'Hello World!'"
        mq.close()

    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()