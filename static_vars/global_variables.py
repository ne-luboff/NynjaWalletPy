# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: global_variables
# Created: 2018-07-16
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>


INFURA_TOKEN = 'oktMAwsvSx2C8gaSg2mg'

# HTTP Endpoints

# Param {0} - Infura Token
# Param {1} - Wallet Address
GET_ACC_BALANCE_ENDPOINT = 'https://api-rinkeby.etherscan.io/api?module=account&action=balance&address={0}&tag=latest&apikey={1}'
GET_ACC_TRANSFER_HISTORY_ENDPOINT = 'https://api-rinkeby.etherscan.io/api?module=account&action=txlist&address={0}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={1}'

GET_ACC_BALANCE = GET_ACC_BALANCE_ENDPOINT.format('{0}', INFURA_TOKEN)
GET_ACC_TRANSFER_HISTORY = GET_ACC_TRANSFER_HISTORY_ENDPOINT.format('{0}', INFURA_TOKEN)

CHECK_ROPSTEN_ADDR = 'https://m6b19m0fxh.execute-api.eu-west-1.amazonaws.com/dev/status'

# Param {0} - Wallet Address
ASK_ROPSTEN_COINS = 'https://m6b19m0fxh.execute-api.eu-west-1.amazonaws.com/dev/ask?address={0}'