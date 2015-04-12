__author__ = 'jdomsic'

from flask import Flask


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE = 'localhost', 27017
    MQ_URL = 'localhost'
    APP_ID = 'default_app_id'
    LOG = 'log_file.txt'
    EXCHANGE = 'default'
    ROLES = ['default_role_1', 'default_role_2']
    DATA_SCHEME_KEY = 'module'
    DATA_SCHEME = {
        'TYPE': ''

    }


class ProductionConfig(Config):
    DATABASE = 'localhost', 27017
    MQ_URL = 'amqp://wizard:wizard@localhost:5672/%2F'
    ROLES = ['upload']
    LOG = '/var/log/gdas/wizard/wizard_01.log'
    EXCHANGE = 'primary'
    APP_ID = 'master_publisher'


app = Flask(__name__)
app.config.from_object(ProductionConfig)

