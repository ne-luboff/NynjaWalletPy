# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: wallet
# Created: 2018-07-12
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>
import logging
from api.example_data import get_wallet_balance_response, put_wallet_response

from base import BaseHandler
from static.global_string import MISSED_REQUIRED_PARAMS, INVALID_FIELD_FORMAT, INVALID_FIELD_FORMAT_DETAILS

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

        print(required_params['password'])

        # check is a string
        if not isinstance(required_params['password'], str):
            return self.failure(message=INVALID_FIELD_FORMAT.format(INVALID_FIELD_FORMAT_DETAILS.format('password',
                                                                                                        'string')))

        response = put_wallet_response()
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

        response = get_wallet_balance_response()

        return self.success(response)