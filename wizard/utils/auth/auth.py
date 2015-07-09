__author__ = 'jdomsic'

class Auth(object):
    def __init__(self, request):
        self.username = getattr(request, 'username', None)
        self.password = getattr(request, 'password', None)
