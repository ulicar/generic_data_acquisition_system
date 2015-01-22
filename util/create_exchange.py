__author__ = 'jdomsic'

import pika

EXCHANGE = 'simple'
TYPE = 'fanout'  # == broadcast
URL = 'localhost'
QUEUE = 'master'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=URL))

channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE, type=TYPE, durable=True)
channel.queue_declare(queue=QUEUE, durable=True)
channel.queue_bind(exchange=EXCHANGE, queue=QUEUE)

connection.close()

