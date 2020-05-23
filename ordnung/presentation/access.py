# -*- coding: utf-8 -*-

"""Tools, that rely on request contents.
"""
import os
import socket
from datetime import date, datetime

from starlette.requests import Request


def get_lang(request: Request) -> str:
    """Extract user language from request.

    We rely on a query string more than on user settings.

    Example output:
        'RU'
    """
    if (lang := request.query_params.get('lang')) is None:
        lang = request.user.lang

    return lang


def get_date(request: Request) -> date:
    """Extract date from request arguments.

    Example output:
        date(2020, 5, 3)
    """
    if (string := request.query_params.get('date')) is not None:
        target_date = datetime.strptime(string, "%Y-%m-%d").date()
    else:
        target_date = datetime.today().date()

    return target_date


def get_local_ip() -> str:
    """Find out which local IP is, so we can broadcast to the LAN.
    """
    if os.name == 'nt':
        ip = socket.gethostbyname(socket.gethostname())

    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # noinspection PyBroadException
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()

    return ip
