__author__ = 'jdomsic'

import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description='Data Collector parser')
    parser.add_argument('-ini', help='Configuration file', metavar='INI')

    return parser.parse_args()