# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: handlers
# Created: 2018-07-20
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import datetime

from base import BaseHandler


class IndexHandler(BaseHandler):
    allowed_methods = ('GET', )

    def get(self):
        return self.success({
            "current_time": datetime.datetime.now().isoformat()
        })

    def put(self):
        return self.failure({
            "current_time": datetime.datetime.now().isoformat()
        })