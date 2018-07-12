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

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        self.finish(self.failure_data(self._reason, status_code))

    def success(self, data=None):
        response = {
            'status': 200
        }

        if data is not None:
            response.update(data)

        logger.debug('Success: {0}'.format(response))
        self.write(response)

    def failure(self, message=None, status=403):
        self.write_error(self.failure_data(message, status))

    @staticmethod
    def failure_data(message, status):
        response = {
            'status': status
        }

        if message:
            response['message'] = message

        logger.debug('Error: {0}'.format(response))
        return response


class Default404Handler(BaseHandler):
    # Override prepare() instead of get() to cover all possible HTTP methods.
    def prepare(self):
        self._reason = "Not Found"
        self.write_error(404)