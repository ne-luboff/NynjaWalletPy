# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: manage.py
# Created: 2018-07-11
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import logging
import sys
from blockchain.connect import blockchain_connection
from run import start_server
from environment import env
from optparse import OptionParser, OptionGroup

LOG_FORMAT = '[%(asctime)s] %(levelname)s [line:%(lineno)s] [%(funcName)s] %(message)s'
logging.basicConfig(format=LOG_FORMAT)

logger = logging.getLogger(__name__)


class ApiManager(object):

    def __init__(self, argv):
        parser = OptionParser(
            usage="manage.py [options] mode",
            description='ORLY!'
        )
        mode_group = OptionGroup(parser, "Mode options (only specify one)")
        parser.add_option_group(mode_group)

        parser.add_option('-d', '--debug', action='store_true', help='Display debug output')
        parser.add_option('-f', '--force', action='store_true', help='Force action')

        (self.options, self.args) = parser.parse_args(argv)
        if len(self.args) == 1:
            print >>sys.stderr, parser.description + '\n'
            print >>sys.stderr, 'Usage:', parser.usage
            print >>sys.stderr, "Modes:"
            for i in filter(lambda i: i.startswith('do_'), dir(self)):
                f = getattr(self, i)
                print >>sys.stderr, "\t%s: %s" % (i[3:], f.__doc__)
            sys.exit()

        self.debug = self.options.debug or env['debug']
        self.force = self.options.force

        env['debug'] = self.debug

        if self.debug:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        getattr(self, 'do_' + self.args[1])(*self.args[2:])

    def do_run(self):
        """
        Runs server
        """
        blockchain_connection()
        start_server()

    def do_connect(self):
        """
        Connect to blockchain network
        """
        blockchain_connection()

if __name__ == '__main__':
    ApiManager(sys.argv)