# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: history
# Created: 2018-07-12
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import logging
from api.example_data import put_wallet_history_response
from base import BaseHandler
from static.global_string import MISSED_REQUIRED_PARAMS

logger = logging.getLogger(__name__)


class WalletHistoryHandler(BaseHandler):
    allowed_methods = ('GET', )

    def get(self):
        """
        Get transfer history
        """
        logger.info("WalletHistory/Get: {0}".format(self.request.arguments))

        required_param_names = ['address']
        required_params = self.get_request_params(required_param_names, query_param=True)

        # check for missing params
        missed_param_names = self.missing_required_params(required_param_names, required_params)
        if missed_param_names:
            return self.failure(message=MISSED_REQUIRED_PARAMS.format(', '.join(missed_param_names)))

        response = put_wallet_history_response(required_params['address'])

        return self.success(response)