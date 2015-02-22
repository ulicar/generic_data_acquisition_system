__author__ = 'jdomsic'

"""
    Helper classes from handling Rabbit MQ consuming.
    If message is not acknowledged or rejected, it will stay in the queue as
    "unacknowleged" <- in limbo :/

    Example usage:
        settings = Settings('amqp://guest:guest@localhost:5672/%2F',
                'example-queue'
        )

        consumer = Consumer(settings)

        def callback(message):
            print str(message)
            # OPTIONAL 1: consumer.acknowledge_msg()
            # OPTIONAL 2: consumer.reject_msg()

        consumer.consume(callback)


    Additional:
        Raises RuntimeError Exception on wrong MQ configuration(wrong queue name).
        Message queue must exist previous to "consume" call.
        If connection to drops/fails, it will try to reconnect.
"""


import pika
import pika.exceptions
import time

from envelope import Envelope


class Settings(object):
    def __init__(self, mq_url, queue, max_messages=1, timeout=2):
        self.mq_url = mq_url
        self.queue = queue
        self.reconnect_time = timeout
        self.max_msgs = max_messages


class Consumer(object):
    def __init__(self, settings):
        self.mq_url = settings.mq_url
        self.queue_name = settings.queue
        self.callback = None

        self.connection = None
        self.channel = None
        self.closing = False
        self.consumer_tag = None
        self.message_tag = None

        self.run_connection = True
        self.reconnect_time = settings.timeout

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
        self.channel.add_on_close_callback(self._on_channel_close)
        self._start_consuming()

    def _start_consuming(self):
        self.channel.add_on_cancel_callback(self._on_consumer_cancelled)

        self.consumer_tag = \
            self.channel.basic_consume(self._on_message_received, self.queue_name)

    def _on_message_received(self, _unused_channel, basic_deliver, properties, body):
        self.message_tag = basic_deliver.delivery_tag

        message, m_type = Envelope.unpack(body)
        self.callback(message, m_type, properties)

    def _on_consumer_cancelled(self):
        # When consumer is canceled remotely
        if self.channel:
            self.channel.close()

    def _on_channel_close(self, _channel, _reply_code, _reply_text):
        if self.run_connection:
            raise RuntimeError('cannot open channel')

    def _on_connection_closed(self, _connection, _reply_code, _reply_text):
        self.channel = None
        if self.run_connection:
            self.connection.add_timeout(self.reconnect_time, self.reconnect)

    def reconnect(self):
        self.connection.ioloop.stop()
        self.connect()

    def consume(self, on_message_received):
        assert isinstance(on_message_received, callable), "%s is not callable" % str(on_message_received)

        self.callback = on_message_received
        self.connect()

    def acknowledge_msg(self):
        """
        Acknowledge message on MQ. Message will be deleted from MQ.
        :return:
        """
        self.channel.basic_ack(self.message_tag)

    def reject_msg(self):
        """
        Rejects message received from MQ. Message will be re-queued.
        If re-queuing fails, message will be discarded or dead-lettered
        :return: None
        """
        self.channel.basic_reject(self.message_tag, requeue=True)

