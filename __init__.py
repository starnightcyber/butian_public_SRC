#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/3
# @Author  : starnight_cyber
# @Github  : https://github.com/starnightcyber
# @Software: PyCharm
# @File    : __init__.py.py

import ssl
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Do not support ssl and disable warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
timestamp = time.strftime("%Y-%m-%d", time.localtime(time.time()))

if __name__ == '__main__':
    pass
