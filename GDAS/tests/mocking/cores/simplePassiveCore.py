#!/usr/bin/python

__author__ = 'jdomsic'


import ConfigParser
import json
import httplib
import sys

from flask import Flask
from flask import Response

from coreCreator import create_cores

TOKEN = 'aaaaaAAAAAaaaaa'
app = Flask(__name__)
parser = ConfigParser.ConfigParser()
parser.read(sys.argv[1])
cores = create_cores(parser)

@app.route('/<core_name>/fetch', methods=['GET'])
def query(core_name):
    if core_name not in cores:
        return Response(response='No core by that name',
                        status=httplib.BAD_REQUEST
        )

    """
    if 'Token' not in request.headers:
        return Response(response='No authentification token in http headers',
                        status=httplib.UNAUTHORIZED)

    if not request.headers.get('Token') == TOKEN:
        return Response(response='Incorrect token',
                        status=httplib.FORBIDDEN
    )
    """

    c = cores[core_name]
    data = [{
        'core': c.name,
        'data': c.collect()
    }]

    return Response(
        mimetype='application/json',
        response=json.dumps(data, indent=4),
        status=httplib.OK,
    )

if __name__ == '__main__':
    app.run(debug=False)
