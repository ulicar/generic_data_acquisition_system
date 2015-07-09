__author__ = 'jdomsic'

import unittest
from mock import Mock
from GDAS.utils.communication.consumer import Consumer
from GDAS.utils.communication.consumer import Settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.settings = Settings('amqp://gdas:GgdasS@localhost:5672/%2F',
                                 ':queue.routing_key',
                                 2)

    def test_init_method_returns_correct_mq_url(self):
        self.assertEquals('amqp://gdas:GgdasS@localhost:5672/%2F', self.settings.mq_url)

    def test_init_method_returns_correct_queue(self):
        self.assertEquals(':queue.routing_key', self.settings.queue)

    def test_init_method_returns_correct_reconnect_time(self):
        self.assertEquals(2, self.settings.reconnect_time)


class TestConsumer(unittest.TestCase):
    def setUp(self):
        settings = Mock()
        settings.mq_url = 'amqp://gdas:GgdasS@localhost:5672/%2F'
        settings.queue = ':default.key'
        settings.reconnect_time = 2

        self.consumer = Consumer(settings)

    def test_init_method_returns_correct_mq_url(self):
        self.assertEquals('amqp://gdas:GgdasS@localhost:5672/%2F', self.consumer.mq_url)

    def test_init_method_returns_correct_exchange(self):
        self.assertEquals(':default.key', self.consumer.queue_name)

    def test_init_method_returns_correct_reconnect_time(self):
        self.assertEquals(2, self.consumer.reconnect_time)


if __name__ == '__main__':
    unittest.main()
