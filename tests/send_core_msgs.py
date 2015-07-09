__author__ = 'jdomsic'

import sys
import requests



data = sys.stdin.read()

payload = data
r = requests.request('POST', "http://admin:admin@127.0.0.1:5000/pictures", data=payload)