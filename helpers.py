# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: helpers.py
# Created: 2017-07-11
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

# from cookielib import CookieJar
from http.cookiejar import CookieJar
# import CookieJar

import decimal
import json
import datetime
import logging
from pprint import pformat
import urllib
from urllib.parse import urlparse
import random
import urllib.request as urllib2
from tornado import web
import zlib

logger = logging.getLogger(__name__)


class ApiJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()[:19]
        elif hasattr(o, 'isoformat'):
            return o.isoformat()[:19]
        elif isinstance(o, set):
            return list(o)
        elif isinstance(o, decimal.Decimal):
            return '%0.4f' % o
        # elif isinstance(o, Base):
        #     return sa_object_to_dict(o)
        else:
            super(ApiJsonEncoder, self).default(o)


def parse_datetime(s, default=None):
    '''
    >>> parse_datetime('2011-09-29')
    datetime.datetime(2011, 9, 29, 0, 0)
    >>> parse_datetime('2011-09-29T12:02:03')
    datetime.datetime(2011, 9, 29, 12, 2, 3)
    >>> parse_datetime('2011-09-29T12:02:03.001234')
    datetime.datetime(2011, 9, 29, 12, 2, 3, 1234)
    >>> parse_datetime('2011-09-29T12:02:03.1234')
    datetime.datetime(2011, 9, 29, 12, 2, 3, 123400)
    >>> parse_datetime('sdfsdf')
    '''
    fmt = '%Y-%m-%d'
    if 'T' in s:
        fmt += 'T%H:%M:%S'
    if '.' in s:
        fmt += '.%f'

    try:
        return datetime.datetime.strptime(s, fmt)
    except Exception:
        return default


def parse_int(s, default=None):
    try:
        return int(s)
    except:
        return default


class HandlersList(object):
    def __init__(self, prefix, items):
        self.prefix = prefix
        self.items = items

    def build(self, prefix=None):
        prefix = prefix or self.prefix or ''

        res = []
        for r in self.items:
            route = '/' + '/'.join([prefix.strip('/')] + r[0].strip('/').split('/')).strip('/')

            if isinstance(r[1], HandlersList):
                res += r[1].build(route)
            elif isinstance(r[1], str):
                m = r[1].split('.')
                ms, m, h = '.'.join(m[:-1]), m[-2], m[-1]
                m = __import__(ms, fromlist=[m], level=0)
                res.append(tuple([route] + [getattr(m, h)] + list(r[2:])))
            else:
                res.append(tuple([route] + list(r[1:])))

        return res


def make_handlers(prefix, *args):
    res = tuple(HandlersList(prefix, args).build())
    logger.debug('\n' + pformat(res))
    return res


def include(module):
    def load_module(m):
        m = m.split('.')
        ms, m = '.'.join(m), m[-1]
        m = __import__(ms, fromlist=[m], level=0)
        return m

    if isinstance(module, (bytes, str)):
        module = load_module(module)

    routes = []
    for member in dir(module):
        member = getattr(module, member)
        if isinstance(member, type) and issubclass(member, web.RequestHandler) and hasattr(member, 'route_path'):
            route_path, route_params = member.route_path, member.route_params

            if route_params:
                routes.append((route_path, member, route_params))
            else:
                routes.append((route_path, member))
    return HandlersList(None, routes)


def route(path, params=None):
    def decorator(cls):
        cls.route_path = path
        cls.route_params = params
        return cls
    return decorator


USER_AGENTS = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.45 Safari/537.22',
)


hh = urllib2.HTTPHandler()
hsh = urllib2.HTTPSHandler()
#hh.set_http_debuglevel(1)
#hsh.set_http_debuglevel(1)

url_opener = urllib2.build_opener(
    hh,
    hsh,
    urllib2.HTTPCookieProcessor(CookieJar()),
    urllib2.HTTPRedirectHandler())


def open_url(url, encoding=None, params=None, data=None):
    logger.warning('Deprecation warning: Use UrlOpener or RequestHandler.url_opener instead of singleton!')
    random.seed()
    if params:
        url += '?' + urllib.urlencode(params)
    url_parts = urlparse(url)
    request = urllib2.Request(url, headers={
        'User-Agent': random.choice(USER_AGENTS),
        'Referer': '%s://%s/' % (url_parts.scheme, url_parts.netloc),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'UTF-8,*;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        })
    if data:
        response = url_opener.open(request, urllib.urlencode(data))
    else:
        response = url_opener.open(request)
    if response.headers.get('Content-Encoding') == 'gzip':
        data = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
    else:
        data = response.read()
    if encoding:
        data = data.decode(encoding)
    return data, response


class UrlOpener(object):
    def __init__(self, debug=False):
        self._debug = debug

    @property
    def url_opener(self):
        if not hasattr(self, '_url_opener'):
            hh = urllib2.HTTPHandler()
            hsh = urllib2.HTTPSHandler()
            if self._debug:
                hh.set_http_debuglevel(1)
                hsh.set_http_debuglevel(1)
            self._url_opener = urllib2.build_opener(
                hh,
                hsh,
                urllib2.HTTPCookieProcessor(CookieJar()),
                urllib2.HTTPRedirectHandler())
        return self._url_opener

    def open_url(self, url, encoding=None, params=None, data=None):
        random.seed()
        if params:
            url += '?' + urllib.urlencode(params)
        url_parts = urlparse(url)
        request = urllib2.Request(url, headers={
            'User-Agent': random.choice(USER_AGENTS),
            'Referer': '%s://%s/' % (url_parts.scheme, url_parts.netloc),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            })
        if data:
            response = self.url_opener.open(request, urllib.urlencode(data))
        else:
            response = self.url_opener.open(request)
        if response.headers.get('Content-Encoding') == 'gzip':
            data = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
        else:
            data = response.read()
        if encoding:
            data = data.decode(encoding)
        return data, response