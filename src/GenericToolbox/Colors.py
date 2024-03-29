#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Color strings

resetColor = "\033[00m"
goldColor = "\033[1;33m"
redColor = "\033[1;31m"
greenColor = "\033[1;32m"
blueColor = "\x1b[94m"
purpleColor = "\033[1;35m"
lightBlueColor = "\x1b[36m"


# Colored message

error = redColor + "<Error>" + resetColor
alert = purpleColor + "<Alert>" + resetColor
warning = goldColor + "<Warning>" + resetColor
info = greenColor + "<Info>" + resetColor
debug = blueColor + "<Debug>" + resetColor
trace = blueColor + "<Trace>" + resetColor
