__author__ = 'jdomsic'

import sys
import ConfigParser
sys.path.append("..")

from utils.input.argument_parser import get_arguments


def main():
    args = get_arguments()
    ini_file = args.ini

    try:
        config = ConfigParser.ConfigParser()
        config.read(ini_file)

        # service, connect to MQ
        print "OK"

    except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()