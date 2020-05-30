# -*- coding: utf-8 -*-

"""Tools, that rely on request contents.
"""
from datetime import date, datetime

from starlette.requests import Request
from itsdangerous import URLSafeSerializer
from werkzeug.security import generate_password_hash

from ordnung import settings
from ordnung.core.access import get_today, get_monotonic
from ordnung.storage.access import get_user_by_id
from ordnung.storage.database import session


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


def send_restore_link(request: Request, user_id: int, email: str):
    # TODO
    auth_s = URLSafeSerializer(settings.SECRET_KEY, salt="restore_password")
    token = auth_s.dumps({"user_id": user_id, "monotonic": get_monotonic()})
    base_url = request.url_for('restore_password', token=token)
    return base_url


def change_user_password(user_id: int, new_password: str):
    user = get_user_by_id(user_id)
    if user is not None:
        user.password = generate_password_hash(new_password)
        session.add(user)
        session.commit()
        return True
    return False
