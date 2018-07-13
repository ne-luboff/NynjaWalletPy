# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: helpers
# Created: 2018-07-13
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

from mnemonic import Mnemonic


def gen_mnemonic_phrase():
    m = Mnemonic('english')
    phrase_words = m.generate()
    phrase_list = phrase_words.split(" ")
    return phrase_list