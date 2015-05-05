__author__ = 'jdomsic'

import json
import sys
import requests


def send_request(data):
    requests.request(
        method='POST',
        url="http://jdomsic:jdomsic@127.0.0.1:5000/wizard/upload",
        data=json.dumps(data)
    )


msgs = list()
for msg in sys.stdin:
    msgs.append(msg)

    i = 1
    if len(msgs) > 3:
        send_request(msgs)
        msgs = []

        print 'SENT %d' % i,
        sys.stdout.flush()
        i += 1

if len(msgs) > 0:
    send_request(msgs)