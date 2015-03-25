__author__ = 'jdomsic'

import argparse
import hashlib
import sys
import pymongo


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
        metavar='ROLES',
        nargs='*',
        default='basic'
    )

    parser.add_argument(
        'admin-username',
        metavar='ADMINUSERNAME',
        help='Username for admin user)'
    )

    parser.add_argument(
        'admin-password',
        metavar='ADMINPASS',
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
        default='master.users'
    )

    return parser.parse_args()


def open_db_connection(args):
    db_url = args['--database']
    db_name, conn_name = args['--collection'].split('.')

    db_client = pymongo.MongoClient(db_url)
    db = db_client[db_name]
    collection = db[conn_name]

    return collection


def create_new_user(args, connection):
    username = args['user_name']
    password = hashlib.sha1(args['password'])
    description = args['user-descr']
    user_roles = set(args['--user-roles'])

    user = users_pb2.user_t()
    user.username = username
    user.password = password
    user.description = description
    user.user_roles.update(user_roles)

    connection.insert(user)


def main():
    args = get_arguments()

    conn = open_db_connection(args)
    create_new_user(args, conn)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)
