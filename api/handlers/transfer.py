# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: transfer
# Created: 2018-07-12
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import logging
from api.example_data import patch_transaction_response
from base import BaseHandler
from static.global_string import MISSED_REQUIRED_PARAMS

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

        response = patch_transaction_response()

        return self.success(response)