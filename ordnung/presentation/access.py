# -*- coding: utf-8 -*-

"""Tools, that rely on request contents.
"""
from datetime import date, datetime

from starlette.requests import Request

from ordnung.core.access import get_today, get_monotonic, generate_token


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
        target_date = get_today()

    return target_date


def send_restore_email(request: Request, user_id: int, email: str) -> str:
    token = generate_token(
        payload={'user_id': user_id, 'monotonic': get_monotonic()},
        salt='restore_password'
    )
    base_url = request.url_for('restore_password', token=token)
    # todo
    print('send_restore_email', base_url, email)
    return base_url


def send_verification_email(request: Request, user_id: int, email: str) -> str:
    """Send link with activation URL to the user.
    """
    token = generate_token(
        payload={'user_id': user_id, 'monotonic': get_monotonic()},
        salt='confirm_registration'
    )
    base_url = request.url_for('register_confirm', token=token)
    # todo
    print('send_verification_email', base_url, email)
    return base_url
