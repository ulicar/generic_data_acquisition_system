__author__ = 'jdomsic'

import sys

from config import Configuration
from config import Logger
from flask import Flask

def init():
    app = Flask(__name__)
    app.cfg = Configuration().load_from_file(sys.argv[1])
    app.logger.addHandler(Logger().create_logger(sys.argv[1]))

    return app

app = init()