__author__ = 'jdomsic'

import argparse
import hashlib
import sys

from GDAS.utils.database.connection import Fatty
from GDAS.utils.security.auth import UserAuth


def get_arguments():
    parser = argparse.ArgumentParser(description='Create users for GDAS')

    parser.add_argument(
        'user_name',
        metavar='USERNAME',
        required=True,
        help='Username for new user'
    )

    parser.add_argument(
        'password',
        metavar='PASSWORD',
        required=True,
        help='Password for new user'
    )

    parser.add_argument(
        'user-descr',
        metavar='USERDECSRIPTION',
        required=True,
        help='Description for new user'
    )

    parser.add_argument(
        '--user-roles',
        metavar='ROLES',
        nargs='*',
        default='basic'
    )

    parser.add_argument(
        'admin-username',
        metavar='ADMINUSERNAME',
        required=True,
        help='Username for admin user)'
    )

    parser.add_argument(
        'admin-pass',
        metavar='ADMINPASS',
        required=True,
        help='Password for admin user'
    )

    parser.add_argument(
        '--database',
        metavar='DATABASE',
        help='Database in form localhost:80',
        default='localhost:27017'
    )

    parser.add_argument(
        '--collection',
        metavar='COLLECTION',
        help='DB Collection in form db.collection',
        default='gdas/accounts'
    )

    return parser.parse_args()


def main():
    args = get_arguments()

    username = args['user_name']
    password = hashlib.sha1(args['password'])
    description = args['user_descr']
    user_roles = set(args['user_roles'])

    user = {
        'username': username,
        'password': password,
        'descr': description,
        'roles': user_roles
    }

    auth = UserAuth()
    if not auth.is_admin(args['admin_username'], args['admin_pass']):
        raise Exception('Only admin can add users')

    url = args['database'].split(':')
    db = Fatty(url)
    db.open(args['collection'])

    db.write(user)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)
