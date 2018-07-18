# -*- coding: utf-8 -*-
#
# Project name: NynjaWalletPy
# File name: js_helper
# Created: 2018-07-18
#
# Author: Liubov M. <liubov.mikhailova@gmail.com>

import execjs
import os


def test():
    path_to_script = os.path.abspath("js_scripts/test.js_scripts")
    with open(path_to_script, 'r') as jsfile:
        script = jsfile.read()
    print(script)
    print("----")
    ctx = execjs.compile(script)
    return ctx.call("add", 1, 2)

if __name__ == "__main__":
    print(test())