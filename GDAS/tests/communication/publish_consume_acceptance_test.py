#!/usr/bin/python

__author__ = 'jdomsic'


"""
    Tests Consumer and Publisher from Communication module.
    (1) Creates 1 consumer and 1 publisher.
    (2) Publishes data on RabbitMq
    (3) Consumes data from RabbitMq
    (4) Prints 'Test passed'

"""


import time
import sys

from GDAS.utils.communication import publisher
from GDAS.utils.communication import consumer

MQ = 'amqp://guest:guest@localhost:5672/%2F'
MESSAGE = 'string data'
ROUTING_KEY = 'computer.usage.temp'


def callback(msg, data_type, properties, stop_consuption):
    assert msg == MESSAGE, "%s" % msg
    assert data_type == ROUTING_KEY, "%s" % data_type

    print "Test passed."
    stop_consuption()


def create_input():
    in_settings = consumer.Settings(MQ, 'computer')
    input_queue = consumer.Consumer(in_settings)

    return input_queue


def create_output():
    out_settings = \
        publisher.Settings('example', MQ, 'master', ROUTING_KEY)
    output_queue = publisher.Publisher(out_settings)

    return output_queue


def main():
    output_mq = create_output()
    input_mq = create_input()

    output_mq.publish([MESSAGE])
    time.sleep(2)

    input_mq.consume(callback)

    return

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        import traceback
        print >>sys.stderr, str(e)
        traceback.print_exc(file=sys.stderr)
