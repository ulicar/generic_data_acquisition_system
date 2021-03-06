__author__ = 'jdomsic'


"""
    Dead letter exchange are for messages with errors or wrongfully sent msgs.
    A message in that queue can last only 24h (in 84 600 000 ms)

    Creates DURABLE and DIRECT exchanges from EXCHANGES.

    Creates queues from QUEUES. Whore string is a queue name, but right part
    is also used as a routing key.

    Creates bindings between QUEUES and EXCHANGES. (q - queue, e - exchange)


"""

import pika


DEADLETTER = {
    'qDead': 'eDead'
}

EXCHANGES = ['ePrimary', 'eSecondary']

QUEUES = [
    'qDefault.all',
    'qPrimary.usa',
    'qPrimary.unizg',
    'qSecondary.hgk',
    'qSecondary.usa',
    'qSecondary.unizg',
]

BINDINGS = {
    'qDefault.all': 'ePrimary',
    'qPrimary.usa': 'ePrimary',
    'qPrimary.unizg': 'ePrimary',
    'qSecondary.hgk': 'eSecondary',
    'qSecondary.usa': 'eSecondary',
    'qSecondary.unizg': 'eSecondary',
}

username = 'gdas'
password = 'GgdasS'
host = 'localhost'
params = pika.URLParameters('ampq://%s:%s@%s:5672/%%2F' % (username, password, host))
connection = pika.BlockingConnection(parameters=params)
channel = connection.channel()

for q, e in DEADLETTER.items():
    channel.exchange_declare(exchange=e, type='fanout', durable=True)
    channel.queue_declare(queue=q, durable=True, arguments={
        'x-message-ttl': 24 * 60 * 60 * 1000,
        'x-dead-letter-exchange': "eDead"
    })

for ex in EXCHANGES:
    channel.exchange_declare(exchange=ex, type='direct', durable=True)

for qu in QUEUES:
    channel.queue_declare(queue=qu, durable=True, arguments={
        'x-dead-letter-exchange': "eDead"
    })

for qu, ex in BINDINGS.items():
    routing_key = qu.split('.')[1]
    channel.queue_bind(exchange=ex, queue=qu, routing_key=routing_key)

connection.close()
