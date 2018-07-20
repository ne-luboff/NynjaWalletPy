# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: wallet
# Created: 2018-07-12
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import logging
from base import BaseHandler
from helpers.helper import get_wallet_data_js_server, to_hex_data
from helpers.http_helper import get_request
from static_vars.global_string import MISSED_REQUIRED_PARAMS, INVALID_FIELD_FORMAT, INVALID_FIELD_FORMAT_DETAILS
from static_vars.global_variables import GET_ACC_BALANCE

logger = logging.getLogger(__name__)


class WalletHandler(BaseHandler):
    allowed_methods = ('PUT', )

    def put(self):
        """
        Create new wallet
        """
        logger.info("Wallet/Put: {0}".format(self.request_body))

        required_param_names = ['password']
        required_params = self.get_request_params(required_param_names)

        # check for missing params
        missed_param_names = self.missing_required_params(required_param_names, required_params)
        if missed_param_names:
            return self.failure(message=MISSED_REQUIRED_PARAMS.format(', '.join(missed_param_names)))

        # check is a string
        if not isinstance(required_params['password'], str):
            return self.failure(message=INVALID_FIELD_FORMAT.format(INVALID_FIELD_FORMAT_DETAILS.format('password',
                                                                                                        'string')))

        data = get_wallet_data_js_server(required_params['password'])
        if not data:
            self.failure()

        response = {
            'address': to_hex_data(data["address"]),
            'private_key': to_hex_data(data["privateKey"]),
            'mnemonic_phrase': data["seed"].split(" ")
        }

        return self.success(response)


class WalletBalanceHandler(BaseHandler):
    allowed_methods = ('GET', )

    def get(self):
        """
        Get wallet balance
        """
        logger.info("WalletBalance/Get: {0}".format(self.request.arguments))

        required_param_names = ['address']
        required_params = self.get_request_params(required_param_names, query_param=True)

        # check for missing params
        missed_param_names = self.missing_required_params(required_param_names, required_params)
        if missed_param_names:
            return self.failure(message=MISSED_REQUIRED_PARAMS.format(', '.join(missed_param_names)))

        get_balance_response = get_request(GET_ACC_BALANCE.format(required_params['address']))
        if get_balance_response['message'] == "NOTOK":
            return self.failure(message=get_balance_response['result'])

        response = {
            'amount': get_balance_response['result']
        }

        return self.success(response)