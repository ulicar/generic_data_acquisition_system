__author__ = 'jdomsic'

import argparse
import hashlib
import sys

from GDAS.utils.database.connection import Fatty
from GDAS.utils.security.auth import UserAuth

COLLECTION = 'gdas-accounts'
DATABASE = 'localhost:27017'


def get_arguments():
    parser = argparse.ArgumentParser(description='Create users for GDAS')

    parser.add_argument(
        'user_name',
        metavar='USERNAME',
        help='Username for new user'
    )

    parser.add_argument(
        'password',
        metavar='PASSWORD',
        help='Password for new user'
    )

    parser.add_argument(
        'user-descr',
        metavar='USERDECSRIPTION',
        help='Description for new user'
    )

    parser.add_argument(
        '--user-roles',
        metavar='ROLE',
        nargs='*',
        default='basic'
    )

    parser.add_argument(
        'admin-username',
        metavar='ADMINUSERNAME',
        help='Username for admin user)'
    )

    parser.add_argument(
        'admin-pass',
        metavar='ADMINPASS',
        help='Password for admin user'
    )

    return vars(parser.parse_args())


def main():
    args = get_arguments()

    username = args['user_name']
    password = hashlib.sha1(args['password']).hexdigest() +\
               hashlib.sha1(username).hexdigest()
    description = args['user-descr']
    user_roles = set(args['user_roles'])

    auth = UserAuth()
    if not auth.is_admin(args['admin-username'], args['admin-pass']):
        raise Exception('Only admin can add users.')

    user = {
        'username': username,
        'password': password,
        'description': description,
        'roles': list(user_roles)
    }

    url = DATABASE.split(':')
    db = Fatty(url)
    database, collection = COLLECTION.split('-')
    db.open(database, collection)
    db.write(user)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)
