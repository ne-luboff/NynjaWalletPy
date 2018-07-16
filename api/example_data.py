# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: example_data
# Created: 2018-07-12
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>
import random

import string
import time

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Helpers
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from helpers.helper import generate_random_string


def gen_wallet_address():
    return generate_random_string(string.ascii_letters + string.digits, 32)


def get_timestamp():
    return int(round(time.time() * 1000))


def gen_balance():
    return round(random.uniform(0, 100), 2)


def rand_choice(preset_data):
    return random.choice([gen_wallet_address(), preset_data])


def rand_choice_dep(preset_data, prev=None):
    if prev is None:
        return rand_choice(preset_data)
    elif prev is not None and prev == preset_data:
        return gen_wallet_address()
    return preset_data


def gen_history_response_object(address):
    address_from = rand_choice_dep(address)
    return {
        "address_from": address_from,
        "address_to": rand_choice_dep(address, address_from),
        "timestamp": get_timestamp(),
        "amount": gen_balance()
    }

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Responses
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def put_wallet_response():
    mnemonic_phrase = [generate_random_string(string.ascii_letters, random.randint(16, 32)) for i in range(0, 12)]
    return {'address': gen_wallet_address(), 'mnemonic phrase': mnemonic_phrase}


def put_wallet_history_response(address='Test'):
    return {"history": [gen_history_response_object(address) for i in range(0, random.randint(1, 10))]}


def get_wallet_balance_response():
    return {"amount": gen_balance()}


def patch_transaction_response():
    return {"hash_transaction": gen_wallet_address()}