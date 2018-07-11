# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: handlers
# Created: 2018-07-11
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import logging
import datetime
from base import OpenApiHandler
from helpers import route

logger = logging.getLogger(__name__)


@route('test')
class Test(OpenApiHandler):
    allowed_methods = ('GET', )

    def read(self):
        return {
            'info': "Nynja Wallet",
            'current_server_time': datetime.datetime.now().isoformat()
        }