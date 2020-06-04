# -*- coding: utf-8 -*-

"""Tools that rely on request contents.
"""
from datetime import date, datetime
from functools import partial
from typing import Callable

from starlette.requests import Request

from ordnung.core.access import get_today
from ordnung.core.localisation import gettext, translate


def get_gettext(lang: str) -> Callable:
    """Make closure with gettext function.

    We're using primitive localisation system, so no magic here.
    """
    return partial(gettext, lang)


def get_translate(lang: str) -> Callable:
    """Make closure with translate function.

    We're using primitive localisation system, so no magic here.
    """
    return partial(translate, lang)


def get_date(request: Request) -> date:
    """Extract date from request arguments.

    Example output:
        date(2020, 5, 3)
    """
    string = request.query_params.get('date')

    if string is None:
        target_date = get_today()
    else:
        target_date = datetime.strptime(string, "%Y-%m-%d").date()

    return target_date
