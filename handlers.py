# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: handlers.py
# Created: 2017-07-11
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

from base import ApiHandler
from helpers import route


@route('')
class IndexHandler(ApiHandler):
    allowed_methods = ('GET', )

    def read(self):
        return {
            'welcome_message': 'Hello!'
        }
