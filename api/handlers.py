# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: handlers
# Created: 2018-07-12
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import logging
import random
import string
from base import BaseHandler
from helpers import generate_random_string
from static.global_string import MISSED_REQUIRED_PARAMS, INVALID_FIELD_FORMAT, INVALID_FIELD_FORMAT_DETAILS

logger = logging.getLogger(__name__)


class WalletHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT',)

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
            return self.failure(message=INVALID_FIELD_FORMAT.format(INVALID_FIELD_FORMAT_DETAILS.format('password', 'string')))

        # gen dummy response
        address = generate_random_string(string.ascii_letters + string.digits, 32)
        mnemonic_phrase = [generate_random_string(string.ascii_letters, random.randint(16, 32)) for x in range(0, 12)]

        return self.success({'address': address, 'mnemonic phrase': mnemonic_phrase})