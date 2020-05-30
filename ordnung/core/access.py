# -*- coding: utf-8 -*-

"""Access tools, related to the core logic.
"""
import time
from datetime import date, datetime


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
