# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: base
# Created: 2018-07-11
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import logging

import tornado

logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):

    def success(self, data=None):
        response = {
            'status': 200
        }

        if data is not None:
            response.update(data)

        logger.debug('Success: {0}'.format(response))
        self.write(response)

    def failure(self, message=None, status=403):
        response = {
            'status': status
        }

        if message:
            response['message'] = message

        logger.debug('Error: {0}'.format(response))
        self.write(response)