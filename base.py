# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: base.py
# Created: 2017-07-11
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

from io import StringIO

import base64
import json
import logging
import threading
import math
from types import GeneratorType
import sys
from tornado import web, ioloop
import zlib
from environment import env
from helpers import ApiJsonEncoder, parse_datetime, parse_int, UrlOpener
import csv


logger = logging.getLogger(__name__)
USER_ID = 'user-id'
CUSTOMER_ID = 'customer-id'


def die(code):
    raise web.HTTPError(code)


def json_encode(v):
    return json.dumps(v, cls=ApiJsonEncoder, indent=4 if env['debug'] else None) if v is not None else ''


class HttpRedirect(object):
    def __init__(self, url):
        self.url = url


def redirect(url):
    return HttpRedirect(url)


class ThreadableRequestHandler(web.RequestHandler):
    def start_worker(self, *args, **kwargs):
        worker_method = self._worker
        threading.Thread(target=worker_method, args=args, kwargs=kwargs).start()

    def worker(self, *args, **kwargs):
        raise web.HTTPError(501)

    def _worker(self, *args, **kwargs):
        res = None
        try:
            res = self.worker(*args, **kwargs)
        except web.HTTPError as e:
            self.set_status(e.status_code)
        except Exception as e:
            self.exc_info = sys.exc_info()
            logger.error(e.message, exc_info=True)
            self.set_status(500)
        ioloop.IOLoop.instance().add_callback(self.async_callback(self.results, res))

    def results(self, res):
        if isinstance(res, HttpRedirect):
            self.redirect(res.url)
        elif self.get_status() >= 400:
            kw = {}
            if hasattr(self, 'exc_info'):
                kw['exc_info'] = self.exc_info
            self.write_error(self.get_status(), **kw)
        else:
            accept_header = self.request.headers.get('Accept') or ''
            if 'csv' in accept_header:
                self.set_header("Content-Type", "text/csv")
                if isinstance(res, (list, tuple)) and res:
                    csvfile = StringIO()
                    writer = csv.writer(csvfile)
                    if isinstance(res[0], dict):
                        for r in res:
                            writer.writerow(r.values())
                    elif isinstance(res[0], (list, tuple)):
                        for r in res:
                            writer.writerow(r)
                    self.finish(csvfile.getvalue())
                else:
                    self.finish()
            else:
                # return JSON
                if isinstance(res, GeneratorType):
                    res = list(res)

                if isinstance(res, (dict, list, tuple, Base)):
                    self.set_header("Content-Type", "application/json; charset=UTF-8")
                    res = json_encode(res)
                self.finish(res)

    def on_finish(self):
        if hasattr(self, '_session'):
            self._session.remove()


class BaseRequestHandler(ThreadableRequestHandler):
    _ARG_DEFAULT = 'dd3f4da1-4bba-4b22-a3bd-963c74493a44'
    def get_arg(self, name, func=None, default=_ARG_DEFAULT):
        if default == self._ARG_DEFAULT:
            default = {
                int: 0,
                bytes: '',
                }.get(func)
        if func:
            def the_func(x):
                try:
                    return func(x)
                except Exception:
                    return default
        else:
            the_func = lambda x: x
        v = map(the_func, self.get_arguments(name)) or [default]
        return v[0] if len(v) == 1 else v

    def get_arg_datetime(self, name, default=_ARG_DEFAULT):
        return self.get_arg(name, parse_datetime, default)

    def get_arg_int(self, name, default=_ARG_DEFAULT):
        return self.get_arg(name, parse_int, default)

    @property
    def request_object(self):
        if not hasattr(self, '_request_object'):
            b = self.request.body
            if self.request.headers.get('Content-Encoding') == 'gzip':
                b = zlib.decompress(b)
            try:
                self._request_object = json.loads(b)
            except:
                self._request_object = None

        return self._request_object

    @property
    def url_opener(self):
        if not hasattr(self, '_url_opener'):
            self._url_opener = UrlOpener()
        return self._url_opener


class ApiHandler(BaseRequestHandler):
    allowed_methods = ()

    @staticmethod
    def make_error(message=None, status=1):

        response = {
            'status': status
        }

        if message:
            response['message'] = message

        logger.debug('Error: {0}'.format(response))
        return response

    @staticmethod
    def success(data=None, status=0):

        response = {
            'status': status,
        }

        if data:
            response['data'] = data

        logger.debug('Success: {0}'.format(response))
        return response

    def test_auth(self, api_key, api_pass):
        pass

    def test_session(self):
        try:
            auth_type, auth_token = self.request.headers.get('Authorization').split()
            if auth_type != 'Basic':
                return False
            api_key, api_pass = base64.decodestring(auth_token).split(':')
            
            logger.debug('api_key, api_pass = %s, %s', api_key, api_pass)
            if api_key == env['api_key'] and api_pass == env['api_pass']:
                return True
            return False
        except Exception:
            return False

    def _worker(self, method, *args, **kwargs):
        res = None
        try:
            if not self.test_session():
                self.set_header('WWW-Authenticate', 'Basic realm="You shall not pass"')
                self.set_status(401)
            elif method not in self.allowed_methods:
                self.set_status(405)
            else:
                m = {
                    'GET': 'read',
                    'POST': 'create',
                    'PUT': 'update',
                    'DELETE': 'remove',
                    }[method]
                w = getattr(self, m, self.worker)
                res = w(*args, **kwargs)
        except web.HTTPError as e:
            self.set_status(e.status_code)
        except Exception as e:
            self.exc_info = sys.exc_info()
            logger.error(e.message, exc_info=True)
            self.set_status(500)
        ioloop.IOLoop.instance().add_callback(self.async_callback(self.results, res))

    @web.asynchronous
    def get(self, *args, **kwargs):
        self.start_worker('GET', *args, **kwargs)

    @web.asynchronous
    def post(self, *args, **kwargs):
        self.start_worker('POST', *args, **kwargs)

    @web.asynchronous
    def put(self, *args, **kwargs):
        self.start_worker('PUT', *args, **kwargs)

    @web.asynchronous
    def push(self, *args, **kwargs):
        self.start_worker('PUSH', *args, **kwargs)

    @web.asynchronous
    def delete(self, *args, **kwargs):
        self.start_worker('DELETE', *args, **kwargs)


class OpenApiHandler(ApiHandler):
    def test_session(self):
        return True


def paginate(qs, page, page_size):
    count = qs.count()
    if page_size > 0:
        pages = int(math.ceil(float(count) / page_size))
    else:
        pages = 1

    page = max(page, 1)
    page = min(page, pages)

    if page_size > 0:
        qs = qs.limit(page_size)
        if pages:
            qs = qs.offset(page_size*(page-1))

    return {
        'page': page,
        'pages': pages,
        'items_count': count,
    }, qs