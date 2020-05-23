# -*- coding: utf-8 -*-

"""Specific parameters, related to presentation.
"""
from ordnung.presentation.connection import get_local_ip

HOST = get_local_ip()
PORT = 8000
DEBUG = True
RELOAD = True
HTTP_OK = 200
HTTP_POST_REDIRECT_GET = 303
HTTP_UNAUTHORIZED = 401