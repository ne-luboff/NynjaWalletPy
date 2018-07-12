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
from router import get_router

logger = logging.getLogger(__name__)


def start_server():
    app = tornado.web.Application(get_router(), default_handler_class=Default404Handler)
    port = env['port']
    logger.debug('Starting API server at %s' % port)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()