__author__ = 'jdomsic'

import unittest
from mock import Mock
from GDAS.utils.communication.publisher import Publisher
from GDAS.utils.communication.publisher import Settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.settings = Settings('id',
                                 'amqp://gdas:GgdasS@localhost:5672/%2F',
                                 'default',
                                 'routing_key',
                                 2)

    def test_init_method_returns_correct_id(self):
        self.assertEquals('id', self.settings.app_id)

    def test_init_method_returns_correct_mq_url(self):
        self.assertEquals('amqp://gdas:GgdasS@localhost:5672/%2F', self.settings.mq_url)

    def test_init_method_returns_correct_exchange(self):
        self.assertEquals('default', self.settings.exchange)

    def test_init_method_returns_correct_routing_key(self):
        self.assertEquals('routing_key', self.settings.routing_key)

    def test_init_method_returns_correct_timeout(self):
        self.assertEquals(2, self.settings.timeout)


class TestPublisher(unittest.TestCase):
    def setUp(self):
        settings = Mock()
        settings.app_id = 'id'
        settings.mq_url = 'amqp://gdas:GgdasS@localhost:5672/%2F'
        settings.exchange = 'default'
        settings.routing_key = 'routing_key'
        settings.timeout = 2

        self.publisher = Publisher(settings)

    def test_init_method_returns_correct_id(self):
        self.assertEquals('id', self.publisher.app_id)

    def test_init_method_returns_correct_mq_url(self):
        self.assertEquals('amqp://gdas:GgdasS@localhost:5672/%2F', self.publisher.mq_url)

    def test_init_method_returns_correct_exchange(self):
        self.assertEquals('default', self.publisher.exchange)

    def test_init_method_returns_correct_routing_key(self):
        self.assertEquals('routing_key', self.publisher.routing_key)

    def test_init_method_returns_correct_reconnect_time(self):
        self.assertEquals(2, self.publisher.reconnect_time)


if __name__ == '__main__':
    unittest.main()
