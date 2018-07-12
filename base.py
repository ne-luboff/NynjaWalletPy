# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: base
# Created: 2018-07-11
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>
import json

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
            # response.update(data)
            response = data

        logger.debug('Success: {0}'.format(response))
        self.write(response)

    def failure(self, message=None, status=400):
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

    @property
    def request_body(self):
        if self.request.headers.get('Content-Type', None) == 'application/json' and self.request.body:
            return tornado.escape.json_decode(self.request.body)
        return None

    @property
    def request_query_params(self):
        if self.request.arguments:
            return tornado.escape.json_decode(json.dumps({k: self.get_argument(k) for k in self.request.arguments}))
        return None

    # def get_request_params(self, params):
    #     """
    #     Function to get request params and return dict with their values
    #     """
    #     results = dict()
    #
    #     for param in params:
    #         res = None
    #         if self.request_body and param in self.request_body:
    #             res = self.request_body[param]
    #         results[param] = res
    #     return results

    def get_request_params(self, params, query_param=False):
        """
        Function to get request params and return dict with their values
        """
        data = self.request_body
        if query_param:
            data = self.request_query_params
        results = dict()

        for param in params:
            res = None
            if data and param in data:
                res = data[param]
            results[param] = res
        return results

    def missing_required_params(self, expected_param_names, actual_params):
        """
        Check is required params missing. Return name of missing params
        """
        missing_param_names = list()
        for expected_param_name in expected_param_names:
            if actual_params[expected_param_name] != 0:
                if not actual_params[expected_param_name]:
                    missing_param_names.append(expected_param_name)

        return missing_param_names


class Default404Handler(BaseHandler):
    # Override prepare() instead of get() to cover all possible HTTP methods.
    def prepare(self):
        self._reason = "Not Found"
        self.write_error(404)