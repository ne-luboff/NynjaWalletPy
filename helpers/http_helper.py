# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: http_helper
# Created: 2018-07-16
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import logging
import requests

logger = logging.getLogger(__name__)


def get_request(endpoint):
    logger.info("HTTP GET REQUEST: {0}".format(endpoint))
    response = requests.get(endpoint)
    logger.info("HTTP GET RESPONSE: {0}, {1}".format(response.status_code, response.text))
    return response.json()
    print(response)
    print(response.status_code)
    print(requests.codes.ok)
    print(response.text)
    return


def get_server_ip():
    endpoint = "http://checkip.amazonaws.com/"
    response = requests.get(endpoint)
    return response.text.strip()