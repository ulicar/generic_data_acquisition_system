__author__ = 'jdomsic'

import pika

MASTER_EXCHANGE = 'master'
TYPE = 'fanout'  # == broadcast
URL = 'localhost'
QUEUE = 'master'



connection = pika.BlockingConnection(pika.ConnectionParameters(host=URL))

channel = connection.channel()
channel.exchange_declare(exchange=MASTER_EXCHANGE, type=TYPE, durable=True)
channel.queue_declare(queue=QUEUE, durable=True)
channel.queue_bind(exchange=MASTER_EXCHANGE, queue=QUEUE)



connection.close()

