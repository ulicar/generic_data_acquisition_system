__author__ = 'jdomsic'


import datetime

SECONDS_IN_HOUR = 3600


def utc_to_time_key(time):
    date_in = datetime.datetime.strptime(time, '%Y-%M-%DT%H:%m:%s')
    date_out = date_in.strftime('%Y-%M-%D-%H')

    return date_out


def time_resolution(start, end, cores, modules):
    assert isinstance(start, datetime.datetime)
    assert isinstance(end, datetime.datetime)
    assert isinstance(cores, int)
    assert isinstance(modules, int)

    return (start - end).total_seconds() / SECONDS_IN_HOUR / cores / modules
