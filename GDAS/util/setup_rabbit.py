__author__ = 'jdomsic'

import pika

EXCHANGES = ['ePrimary', 'eSecondary', 'eDead']

QUEUES = [
    'qDefault.all',
    'qPrimary.cpu',
    'qPrimary.temp',
    'qSecondary.cpu'
]

BINDINGS = {
    'qDefault.all': 'ePrimary',
    'qPrimary.cpu': 'ePrimary',
    'qPrimary.temp': 'ePrimary',
    'qSecondary.cpu': 'eSecondary',
    'eDead': ''
}

URL = 'localhost'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=URL))
channel = connection.channel()
for ex in EXCHANGES:
    channel.exchange_declare(exchange=ex, type='direct', durable=True)

for qu in QUEUES:
    channel.queue_declare(queue=qu, durable=True)

for qu, ex in BINDINGS.items():
    routing_key = qu.split('.')[1]
    channel.queue_bind(exchange=ex, queue=qu, routing_key=routing_key)


connection.close()
