# -*- coding: utf-8 -*-

"""Access tools, related to the core logic.
"""
import time
from datetime import date, datetime
from typing import Optional, Any, Tuple

from itsdangerous import URLSafeSerializer

from ordnung import settings


def get_today() -> date:
    """Get today's date.
    """
    return date.today()


def get_now() -> datetime:
    """Get current moment.
    """
    return datetime.now()


def get_monotonic():
    """Get current monotonic time.
    """
    return time.monotonic()


def check_token(token: Optional[str], salt: str) -> Tuple[bool, Any]:
    """Check if given token is correct.
    """
    auth_s = URLSafeSerializer(settings.SECRET_KEY, salt=salt)
    sig_okay, payload = auth_s.loads_unsafe(token)
    return sig_okay, payload


def generate_token(payload: dict, salt: str) -> str:
    """Generate new token.
    """
    auth_s = URLSafeSerializer(settings.SECRET_KEY, salt=salt)
    token = auth_s.dumps(payload)
    return token


def token_is_too_old(payload: dict) -> bool:
    """Return True if link is too old and can't be used.
    """
    delta = get_monotonic() - payload.get('monotonic', 0)
    return delta > settings.MAX_PASSWORD_RESTORE_INTERVAL
