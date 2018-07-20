# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: run
# Created: 2018-07-11
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import logging

import tornado.ioloop
import tornado.web
from base import Default404Handler

from environment import env
from router import api_handlers

logger = logging.getLogger(__name__)


def start_server():
    # check is it daemon
    daemon_mode = env.get('daemon', False)
    if daemon_mode is True:
        logfile = open(env['logfile'], 'a+')

        from daemon import pidfile, DaemonContext
        pid = pidfile.TimeoutPIDLockFile(env['pidfile'], 10)
        logger.debug('Pidfile: %s', env['pidfile'])
        ctx = DaemonContext(stdout=logfile, stderr=logfile, working_directory='.', pidfile=pid)
        ctx.open()

    app = tornado.web.Application(api_handlers(), default_handler_class=Default404Handler)
    port = env['port']
    logger.debug('Starting API server at %s' % port)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()