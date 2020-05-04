# -*- coding: utf-8 -*-

"""Tools, related to time operations.
"""
from datetime import datetime, date


def today() -> date:
    """Get today's date.

    :return: stdlib date object, representing this day
    """
    return date.today()
