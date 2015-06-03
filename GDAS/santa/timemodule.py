__author__ = 'jdomsic'


import datetime

SECONDS_IN_HOUR = 3600


def to_datetime(time):
    return datetime.datetime.strptime(time, '%Y-%M-%DT%H:%m:%s')


def to_database_key(date):
    return date.strftime('%Y-%M-%D-%H')


def time_resolution(start, end, cores, modules):
    assert isinstance(start, datetime.datetime)
    assert isinstance(end, datetime.datetime)
    assert isinstance(cores, int)
    assert isinstance(modules, int)

    return (start - end).total_seconds() / SECONDS_IN_HOUR / cores / modules
