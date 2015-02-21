__author__ = 'jdomsic'


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE = 'localhost:27017'
    MESSAGE_QUEUE = 'localhost'
    LOG = 'log_file.txt'
    EXCHANGE = 'default'
    ROLES = ['default_role_1', 'default_role_2']


class ProductionConfig(Config):
    DATABASE = 'localhost:27017'
    ROLES = ['upload']
    LOG = 'utils/logging/file_log.txt'
    EXCHANGE = 'simple'


class DevelopmentConfig(Config):
    DATABASE = 'localhost:27017'
    ROLES = ['upload']
    LOG = 'utils/logging/file_log.txt'
    EXCHANGE = 'simple'


class TestingConfig(Config):
    DATABASE = 'localhost:27017'
    ROLES = ['upload']
    LOG = 'utils/logging/file_log.txt'
    EXCHANGE = 'simple'
