# -*- coding: utf-8 -*-

"""Tools, that rely on request contents.
"""
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
