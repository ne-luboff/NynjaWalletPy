# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: connect
# Created: 2018-07-13
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import logging
from web3 import Web3
from web3.middleware import geth_poa_middleware
from blockchain.helpers import get_blockchain_network_type

INFURA_KEY = 'oktMAwsvSx2C8gaSg2mg'
PUBLIC_NETWORK_NAME = 'rinkeby'
PUBLIC_ENDPOINT_TEMPLATE = 'https://{0}.infura.io/{1}'
# PUBLIC_ENDPOINT_TEMPLATE = 'https://rinkeby.infura.io/oktMAwsvSx2C8gaSg2mg'

PRIVATE_ENDPOINT_TEMPLATE = "http://{0}:{1}"
PRIVATE_NETWORK_IP = "35.198.169.85"
PRIVATE_NETWORK_PORT = "8545"

blockchain_network_connection = None

logger = logging.getLogger(__name__)


def connect_public_network():
    """
    Connect to public blockchain network
    """
    endpoint = PUBLIC_ENDPOINT_TEMPLATE.format(PUBLIC_NETWORK_NAME, INFURA_KEY)
    logger.info("Connect to blockchain network: {0}".format(endpoint))
    w3 = Web3(Web3.HTTPProvider(endpoint))
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)
    global blockchain_network_connection
    blockchain_network_connection = w3
    return blockchain_network_connection


def connect_private_network():
    """
    Connect to private blockchain network
    """
    endpoint = PRIVATE_ENDPOINT_TEMPLATE.format(PRIVATE_NETWORK_IP, PRIVATE_NETWORK_PORT)
    logger.info("Connect to blockchain network: {0}".format(endpoint))
    w3 = Web3(Web3.HTTPProvider(endpoint))
    global blockchain_network_connection
    blockchain_network_connection = w3
    return blockchain_network_connection


def blockchain_connection():
    """
    Get or set blockchain network connection depends on network type
    """
    if not blockchain_network_connection:
        if get_blockchain_network_type():
            connect_private_network()
        else:
            connect_public_network()
    return blockchain_network_connection