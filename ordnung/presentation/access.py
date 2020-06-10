# -*- coding: utf-8 -*-

"""Tools that rely on request contents.
"""
from datetime import date, datetime
from functools import partial
from typing import Callable, List

from starlette.requests import Request

from ordnung import settings
from ordnung.core.access import get_today
from ordnung.core.localisation import gettext, translate


def get_lang(request: Request) -> str:
    """Extract user language from request.
    """
    if request.user.is_authenticated:
        return request.user.parameters.lang
    return extract_language(request)


def extract_language(request: Request) -> str:
    """Extract user language from any part of request we could search for.
    """
    # TODO
    return settings.DEFAULT_LANG


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
    string = request.path_params.get('date')

    if string is None:
        target_date = get_today()
    else:
        target_date = datetime.strptime(string, "%Y-%m-%d").date()

    return target_date


async def get_errors(gettext_callable: Callable,
                     errors_dict: dict) -> List[str]:
    """Extract errors from WTForm.
    """
    errors = []

    for key, value in errors_dict.items():
        name = gettext_callable(key).capitalize()

        for each in value:
            description = gettext_callable(each).capitalize()
            errors.append(f'<strong>{name}</strong><br>{description}')

    return errors
