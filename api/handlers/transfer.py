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

        response = patch_transaction_response()

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