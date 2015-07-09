__author__ = 'jdomsic'

import unittest

from mock import Mock, patch
from wizard.wizard import app


class TestWizard(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('wizard.wizard.requests')
    def test_no_auth_data(self, mock_request):
        mock_request.authorization['username'] = 'username'
        mock_request.authorization['password'] = 'password'
        mock_request.post.status = 401
        mock_request.post.data = 'Wrong username/password'

        auth = Mock()
        auth.authentificate.return_value = False

        self.assertEquals(self.app.post('/upload'), mock_request)

