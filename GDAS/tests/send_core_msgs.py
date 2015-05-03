__author__ = 'jdomsic'

import sys
import requests

data = sys.stdin.read()

payload = data
r = requests.request('POST', "http://jdomsic:jdomsic@127.0.0.1:5000/wizard/upload", data=payload)
