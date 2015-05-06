__author__ = 'jdomsic'

import json
import sys
import requests
import time


def send_request(data):
    requests.request(
        method='POST',
        headers={'Connection': 'close'},
        url="http://jdomsic:jdomsic@127.0.0.1:5000/wizard/upload",
        data=json.dumps(data)
    )


msgs = list()
for msg in sys.stdin:
    msgs.append(json.loads(msg))

    i = 1
    if len(msgs) > 5:
        print 'START - '
        send_request(msgs)
        msgs = []
        print ' END\n'

        time.sleep(1)

if len(msgs) > 0:
    send_request(msgs)