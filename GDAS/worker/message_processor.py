__author__ = 'jdomsic'

import sys
import pika
from config import Configuration

from utils.input.argument_parser import get_arguments


def main():
    args = get_arguments()
    ini_file = args.ini

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='hello')

        print ' [*] Waiting for messages. To exit press CTRL+C'

        def callback(ch, method, properties, body):
            print " [x] Received %r" % (body,)

        channel.basic_consume(callback,
                              queue='hello',
                              no_ack=True)

        channel.start_consuming()

    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()