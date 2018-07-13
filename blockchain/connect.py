# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: connect
# Created: 2018-07-13
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

from web3 import Web3

INFURA_KEY = 'oktMAwsvSx2C8gaSg2mg'
NETWORK_NAME = 'rinkeby'
ENDPOINT_TEMPLATE = 'https://{0}.infura.io/{1}'


def network_connect():
    """
    Connect to blockchain network
    """
    Endpoint = ENDPOINT_TEMPLATE.format(NETWORK_NAME, INFURA_KEY)
    web3 = Web3(Web3.HTTPProvider(Endpoint))
    return web3.version.node