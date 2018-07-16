# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: transfer
# Created: 2018-07-12
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>
import json

import logging
from api.example_data import patch_transaction_response
from base import BaseHandler
from blockchain.connect import get_connection
from blockchain.helpers import checksum
from helpers.http_helper import get_request
from static.global_string import MISSED_REQUIRED_PARAMS, SMTH_WENT_WRONG
from static.global_variables import ASK_ROPSTEN_COINS

logger = logging.getLogger(__name__)


class TransferHandler(BaseHandler):
    allowed_methods = ('PATCH', )

    def patch(self):
        """
        Create new transfer
        """
        logger.info("WalletTransfer/Patch: {0}".format(self.request_body))

        required_param_names = ['address_from', 'address_to', 'amount']
        required_params = self.get_request_params(required_param_names)

        # check for missing params
        missed_param_names = self.missing_required_params(required_param_names, required_params)
        if missed_param_names:
            return self.failure(message=MISSED_REQUIRED_PARAMS.format(', '.join(missed_param_names)))

        key_hex = 'f56d530479dda6cb2a3882f10fc292c30167fcc8a4a6bae39981b63d5f875c04'

        w3 = get_connection()

        transaction = {
            'gasPrice': w3.eth.gasPrice,
            'value': required_params['amount'],
            'to': checksum(required_params['address_to']),
            'nonce': w3.eth.getTransactionCount(checksum(required_params['address_from']))
        }

        gas_estimate = w3.eth.estimateGas(transaction)
        transaction['gas'] = gas_estimate

        key = bytearray.fromhex(key_hex)

        signed = w3.eth.account.signTransaction(transaction, key)
        print(signed.rawTransaction)

        try:
            hash_transaction = w3.eth.sendRawTransaction(signed.rawTransaction)
        except Exception as E:
            logger.info("{0}".format(E))
            return self.failure(message=str(E))

        response = {
            'hash_transaction': hash_transaction
        }

        return self.success(response)


class MintHandler(BaseHandler):
    allowed_methods = ('PATCH', )

    def patch(self):
        """
        Create new mint
        """
        logger.info("WalletMint/Get: {0}".format(self.request_body))

        required_param_names = ['address', 'amount']
        required_params = self.get_request_params(required_param_names)

        # check for missing params
        missed_param_names = self.missing_required_params(required_param_names, required_params)
        if missed_param_names:
            return self.failure(message=MISSED_REQUIRED_PARAMS.format(', '.join(missed_param_names)))

        # check faucet address
        # ask faucet address
        ask_for_coins_response = get_request(ASK_ROPSTEN_COINS.format(required_params['address']))
        print(ask_for_coins_response)
        print(type(ask_for_coins_response))
        if ask_for_coins_response.get("statusCode", 200) != 200:
            error_msg = SMTH_WENT_WRONG
            try:
                error_msg = json.loads(ask_for_coins_response['body'])['message']
            except Exception:
                pass
            return self.failure(message=error_msg)

        response = {
            'hash_transaction': ask_for_coins_response['message']['tx']
        }

        return self.success(response)