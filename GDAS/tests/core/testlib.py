__author__ = 'jdomsic'

import string
import random


def create_random_string(size):
    choices = string.ascii_letters
    return ''.join(random.choice(choices) for _ in range(size))


def create_random_value(a=None, b=None, retval=None):
    assert a is not None, "start must not be None"
    assert retval is not None, "retval must not be None"

    if type(a) is int and type(b) is int:
        return retval(random.randint(a, b))

    if type(a) is str and type(b) is int:
        return create_random_string(b)

    if type(a) is list and type(b) is int:
        assert b, 'Must be bigger than 0'
        if b == 1:
            return random.choice(a)

        return [x for x in a]
