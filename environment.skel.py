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
    'cookie_secret': '',
    'password_salt': '',
    'daemon': False,
    'ssl': False,
    'ws_ssl': False,
    'listen': '0.0.0.0:8000',
    'wslisten': '0.0.0.0:8888',
    'logfile': os.path.join(ROOT, 'NynjaWalletPy.log'),
    'pidfile': os.path.join(ROOT, 'pid'),
    'url_prefix': '',
    'db': 'postgresql://localhost/NynjaWalletPy',
    'site_url': 'http://localhost:8000/',
    'static_url': 'http://localhost:8000/s/',
    'static_path': os.path.join(ROOT, 'static'),
    'serve_static': False,
    'mail': {
        'from': '',
        'subject': 'NynjaWalletPy Password',
        'server': '',
        'login': '',
        'password': ''
    },
}