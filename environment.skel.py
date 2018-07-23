# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: environment.skel.py
# Created: 2018-07-23
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import os

ROOT = os.path.abspath(os.path.dirname(__file__))


env = {
    # debug mode: True / False
    'debug': True,
    # daemon: True / False
    'daemon': False,
    # private_blockchain: True / False
    'private_blockchain': True,
    # port: string, ex: '8000'
    'port': '8000',
    # logfile: name of file for logging, string, by default is 'NynjaWalletPy.log'
    'logfile': os.path.join(ROOT, 'NynjaWalletPy.log'),
    'pidfile': os.path.join(ROOT, 'pid')
}