__author__ = 'jdomsic'

"""
    Helper classes from handling Rabbit MQ publishing.
    Precondition: Message is serialized.

    Example usage:
        settings = Settings('example-app-id',
                'amqp://guest:guest@localhost:5672/%2F',
                'example-exchange',
                'example-routing_key'
        )

        publisher = Publisher(settings)

        publisher.publish(list_of_messages)

    Additional:
        Raises StopIteration Exception when passed empty list_of_messages.
        Raises RuntimeError Exception on wrong MQ configuration(wrong queue name).
        Message queue and exchange must exist previous to "publish" call.
        If connection to drops/fails, it will try to reconnect.
"""

import time

import pika
import pika.exceptions

from envelope import Envelope


class Settings(object):
    """
    :arg app_id Application name
    :arg mq_url Message queue URL, 'ampq://user:pass@host:port/%2F'
    """
    def __init__(self, app_id, mq_url, exchange, routing_key, timeout=2):
        self.app_id = app_id
        self.mq_url = mq_url
        self.exchange = exchange
        self.routing_key = routing_key
        self.timeout = timeout
        self.message_type = None


class Publisher(object):
    def __init__(self, settings):
        self.app_id = settings.app_id
        self.mq_url = settings.mq_url
        self.exchange = settings.exchange
        self.routing_key = settings.routing_key
        self.reconnect_time = settings.timeout

        self.connection = None
        self.channel = None
        self.run_connection = True
        self.message_iterator = None
        self.message = None

    def connect(self):
        while self.run_connection:
            try:
                self.connection = pika.SelectConnection(
                    pika.URLParameters(self.mq_url),
                    self._on_connection_open,
                    stop_ioloop_on_close=False
                )

                self.connection.ioloop.start()

            except pika.exceptions.AMQPConnectionError:
                time.sleep(self.reconnect_time)

    def _on_connection_open(self, _connection):
        self.connection.add_on_close_callback(self._on_connection_closed)

        self.channel = self.connection.channel(on_open_callback=self._on_channel_open)
        self.channel.add_on_close_callback(self._on_channel_close)

    def _on_channel_open(self, _channel):
        self.channel.confirm_delivery(self._on_delivery_confirmation)
        self.start_publishing()

    def start_publishing(self):
        self.channel.confirm_delivery(self._on_delivery_confirmation)
        self.send_msg_to_mq()

    def send_msg_to_mq(self):

        envelope = str(Envelope(self.message, self.routing_key))

        properties = pika.BasicProperties(app_id=self.app_id,
                                          content_type='text/plain',
                                          delivery_mode=2)

        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.routing_key,
                                   body=envelope,
                                   properties=properties)

    def _on_delivery_confirmation(self, method_frame):
        if 'ack' != method_frame.method.NAME.split('.')[1].lower():
            self.send_msg_to_mq()
        else:
            try:
                self.message = self.message_iterator.next()
                self.send_msg_to_mq()

            except StopIteration:
                self.stop()

                return

    def stop(self):
        self.run_connection = False
        self.channel.close()
        self.connection.close()
        self.connection.ioloop.stop()

    def _on_channel_close(self, _channel, _reply_code, _reply_text):
        if self.run_connection:
            raise RuntimeError('cannot open channel')

    def _on_connection_closed(self, _connection, _reply_code, _reply_text):
        self._channel = None

        if self.run_connection:
            self.connection.add_timeout(self.reconnect_time, self.reconnect)

    def reconnect(self):
        self.connection.ioloop.stop()
        self.connect()

    def publish(self, messages, routing_key=None):
        """ Raises StopIteration Exception on empty iterator """
        if routing_key is not None:
            self.routing_key = routing_key

        self.message_iterator = iter(messages)
        self.message = self.message_iterator.next()
        self.connect()
