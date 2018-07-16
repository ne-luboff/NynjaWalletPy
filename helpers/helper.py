# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: helpers
# Created: 2018-07-12
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import random
import string


def generate_random_string(allowed_symbols=None, length=16):
    """
    Generate random string.
    Mode - which symbols will be used (according to RandomStringGeneratorModeEnum),
    Length - length of generated string
    """

    if not allowed_symbols:
        allowed_symbols = string.digits

    return ''.join(random.choice(allowed_symbols) for _ in range(length))