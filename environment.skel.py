# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: environment.py
# Created: 2017-07-11
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import os

ROOT = os.path.abspath(os.path.dirname(__file__))


env = {
    'debug': True,
    'api_key': '',
    'api_pass': '',
    'cookie_secret': '',
    'password_salt': '',
    'daemon': False,
    'ssl': False,
    'port': '8000',
    'logfile': os.path.join(ROOT, 'NynjaWalletPy.log'),
    'pidfile': os.path.join(ROOT, 'pid'),
    'url_prefix': '',
    'serve_static': False
}