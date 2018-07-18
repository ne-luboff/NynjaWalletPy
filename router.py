# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: router
# Created: 2018-07-11
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

from api.handlers.history import WalletHistoryHandler
from api.handlers.transfer import TransferHandler, MintHandler
from api.handlers.wallet import WalletHandler, WalletBalanceHandler, GenWalletHandler
from handlers import IndexHandler


def get_router():
    return [
        (r"/", IndexHandler),
        (r"/wallet", WalletHandler),
        (r"/wallet/balance", WalletBalanceHandler),
        (r"/wallet/history", WalletHistoryHandler),
        (r"/transfer", TransferHandler),
        (r"/mint", MintHandler),
        (r"/gen", GenWalletHandler)
    ]