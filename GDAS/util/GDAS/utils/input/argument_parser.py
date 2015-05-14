__author__ = 'jdomsic'

import argparse


def argument_parser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--ini', help='Configuration file', metavar='INI')

    return parser.parse_args()
