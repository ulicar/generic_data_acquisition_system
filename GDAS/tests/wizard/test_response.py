__author__ = 'jdomsic'

import unittest
from wizard.message_collector import check_format


class wizard_unit_test(unittest.TestCase):

    def test_check_format__good_format(self):
        data = {}
        check_format()
