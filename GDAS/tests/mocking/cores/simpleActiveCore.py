#!/usr/bin/python

__author__ = 'jdomsic'


"""
    Mocks a CORE.

    Prints out all sensor data (changed) every second.
    (4x Temp, 3x Humidity, 2x Cpu, 2x Light senors.)
"""

import ConfigParser
import json
import sys
import time
import requests

from multiprocessing import Pool

from coreCreator import create_cores

TOKEN = 'aaaaaAAAAAaaaaa'
parser = ConfigParser.ConfigParser()
parser.read(sys.argv[1])
cores = create_cores(parser).values()
push_flag = True if len(sys.argv) > 2 and '--push' in sys.argv else False
run_for = int(sys.argv[4]) if len(sys.argv) > 2 and '--run-for' in sys.argv else 1
START = time.time()


def main():
    p = Pool(len(cores))
    p.map(get_data, cores)


def get_data(core):
    while True:
        if time.time() >= START + run_for:
            break

        data = [{
            'core': core.name,
            'data': core.collect()
        }]

        if push_flag:
            send_request(json.dumps(data, indent=4))
            print 'Data sent to server.'

        else:
            print data

        time.sleep(0.97)


def send_request(data):
    auth_token = 'aaaaaAAAAAaaaaa'

    requests.request(
        method='POST',
        headers={
            'Connection': 'close',
            'token': auth_token,
            'Content-Type': 'application/json'
            },
        url="http://jdomsic:jdomsic@localhost:5000/upload",
        data=data
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print >>sys.stderr, str(e)
