# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: app.py
# Created: 2017-07-11
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import os
from tornado import web
from environment import env
from helpers import make_handlers, include


ROOT = os.path.abspath(os.path.dirname(__file__))


class NynjaWalletPyApi(web.Application):
    def __init__(self, handlers = None, default_host = "", transforms = None, wsgi = False, **settings):
        super(NynjaWalletPyApi, self).__init__(self.get_handlers(), **{
            'cookie_secret': env['cookie_secret'],
            'debug': env['debug'],
            })

    def get_handlers(self):
        res = make_handlers(env.get('url_prefix', ''),
            (r'/api/', include('api.handlers')),
            (r'', include('handlers')),
        )
        return res