# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: helpers
# Created: 2018-07-13
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

from mnemonic import Mnemonic
from web3 import Web3


def gen_mnemonic_phrase():
    m = Mnemonic('english')
    phrase_words = m.generate()
    phrase_list = phrase_words.split(" ")
    return phrase_list


def checksum(adr):
    if not Web3.isChecksumAddress(adr):
        adr = Web3.toChecksumAddress(adr)
    return adr