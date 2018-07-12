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
        print('here i am')
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            print(1)
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            # for line in traceback.format_exception(*kwargs["exc_info"]):
            #     self.write(line)
            self.finish()
        else:
            print(2)
            self.finish(self.failure_data(self._reason, status_code))
            # self.finish("<html><title>qqqqqqqqq%(code)d: %(message)s</title>"
            #             "<body>%(code)d: %(message)s</body></html>" % {
            #                 "code": status_code,
            #                 "message": self._reason,
            #             })

    def success(self, data=None):
        response = {
            'status': 200
        }

        if data is not None:
            response.update(data)

        logger.debug('Success: {0}'.format(response))
        self.write(response)

    def failure(self, message=None, status=403):
        self.set_status(status)
        self.write(self.failure_data(message, status))

    @staticmethod
    def failure_data(message, status):
        response = {
            'status': status
        }

        if message:
            response['message'] = message

        logger.debug('Error: {0}'.format(response))
        return response