# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: http_helper
# Created: 2018-07-16
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>
import json

import logging
import requests

logger = logging.getLogger(__name__)


def get_request(endpoint):
    logger.info("HTTP GET REQUEST: {0}".format(endpoint))
    response = requests.get(endpoint)
    logger.info("HTTP GET RESPONSE: {0}, {1}".format(response.status_code, response.text))
    # try to parse json
    try:
        return response.json()
    except Exception as e:
        logger.info("Exception:{0}".format(str(e)))
        return None


def post_request(endpoint, data, headers):
    logger.info("HTTP POST REQUEST: {0}".format(endpoint))
    response = requests.post(endpoint, data=json.dumps(data), headers=headers)
    logger.info("HTTP POST RESPONSE: {0}, {1}".format(response.status_code, response.text))
    # try to parse json
    try:
        return response.json()
    except Exception as e:
        logger.info("Exception:{0}".format(str(e)))
        return None


def get_server_ip():
    endpoint = "http://checkip.amazonaws.com/"
    response = requests.get(endpoint)
    return response.text.strip()