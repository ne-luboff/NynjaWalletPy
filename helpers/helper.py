# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: helpers
# Created: 2018-07-12
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import logging
import os
import random
import string
import platform
from selenium import webdriver
import time

logger = logging.getLogger(__name__)

def generate_random_string(allowed_symbols=None, length=16):
    """
    Generate random string.
    Mode - which symbols will be used (according to RandomStringGeneratorModeEnum),
    Length - length of generated string
    """

    if not allowed_symbols:
        allowed_symbols = string.digits

    return ''.join(random.choice(allowed_symbols) for _ in range(length))


def get_wallet_data(password=None):
    url = "http://127.0.0.1:8888/gen?p={0}".format(password)
    driver_name = "chromedriver_linux_64"

    if platform.system() == 'Darwin':
        driver_name = "chromedriver_mac_64"

    try:
        driver = webdriver.Chrome(executable_path=os.path.abspath("drivers/{0}".format(driver_name)))
        driver.get(url)
        time.sleep(5)
        data_element = driver.find_element_by_css_selector("#data")
        data = data_element.text
        driver.close()
        return data
    except Exception as E:
        logger.info("GenWalletError: {0}".format(str(E)))

    return None