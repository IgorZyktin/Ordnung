# -*- coding: utf-8 -*-

"""Tools that rely on request contents.
"""
import urllib
from datetime import date, datetime

from starlette.requests import Request

from ordnung.core.access import get_today, get_monotonic, generate_token
from ordnung import settings
from ordnung.presentation.email_sending import send_email


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


def url_for(request: Request, *args, **kwargs) -> str:
    """Wrapper for the standard url_for, that gives absolute/relative links.
    """
    base_url = request.url_for(*args, **kwargs)
    if settings.URL_STYLE == 'absolute':
        return base_url

    segments = urllib.parse.urlparse(base_url)
    return ''.join(segments[2:])


def send_restore_email(request: Request, user_id: int, email: str) -> str:
    """Send link with password restore URL to the user.
    """
    token = generate_token(
        payload={'user_id': user_id, 'monotonic': get_monotonic()},
        salt='restore_password'
    )
    base_url = url_for(request, 'restore_confirm', token=token)
    # todo
    send_email('Password restore', [email], f'Your password restore link: http://84.201.137.8/{base_url}')
    return base_url


def send_verification_email(request: Request, user_id: int, email: str) -> str:
    """Send link with account activation URL to the user.
    """
    token = generate_token(
        payload={'user_id': user_id, 'monotonic': get_monotonic()},
        salt='confirm_registration'
    )
    base_url = url_for(request, 'register_confirm', token=token)
    # todo
    send_email('Registration confirm', [email], f'Your confirmation link: http://84.201.137.8/{base_url}')
    return base_url
