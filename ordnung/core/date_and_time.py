# -*- coding: utf-8 -*-

"""Tools, related to time operations.
"""
from datetime import date, timedelta
from typing import Tuple, List

from ordnung import settings


class Day:
    """Representation of a single day in month table.
    """

    def __init__(self, current_date: date, is_today: bool = False) -> None:
        """Initialize instance.
        """
        self.origin_date = current_date
        self.date = str(current_date)
        self.weekday = current_date.weekday()
        self.number = current_date.day
        self.month = current_date.month
        self.year = current_date.year
        self.is_today = is_today
        self.is_weekend = self.weekday in settings.WEEKENDS

    def __repr__(self) -> str:
        """Textual representation.
        """
        return f'{type(self).__name__}({self.date})'

    @property
    def css_class(self) -> str:
        """Form visualisation class.
        """
        css_class = 'day'

        if self.is_today:
            css_class += ' today'

        if self.is_weekend:
            css_class += ' weekend'

        return css_class


def get_offset_dates(target_date: date) -> Tuple[date, date, date, date]:
    """Calculate target dates that we will jump on step/leap forward/back.

    leap_back  step_back  today  step_forward  leap_forward
        │         │         │         │             │       Default parameters:
        │         │         │         │             └────── today + 21 day
        │         │         │         └──────────────────── today + 7 days
        │         │         └────────────────────────────── today
        │         └──────────────────────────────────────── today - 7 days
        └────────────────────────────────────────────────── today - 21 day

    Example output:
        [date(2020, 4, 12), date(2020, 4, 26), date(2020, 5, 10), ...]
    """
    leap_back = target_date - timedelta(days=settings.LEAP_SIZE)
    step_back = target_date - timedelta(days=settings.STEP_SIZE)
    step_forward = target_date + timedelta(days=settings.STEP_SIZE)
    leap_forward = target_date + timedelta(days=settings.LEAP_SIZE)

    return leap_back, step_back, step_forward, leap_forward


def form_month(current_date: date) -> List[Day]:
    """Form contents for the main table.

    Example output:
        [
            Day(2020-05-04),
            Day(2020-05-05),
            Day(2020-05-06),
            Day(2020-05-07),
            ...
        ]
    """
    weekday = current_date.weekday()
    index = settings.WEEK_LENGTH * 2 + weekday

    month: List[Day] = [None] * settings.WEEK_LENGTH * settings.WEEKS_IN_MONTH
    month[index] = Day(current_date, is_today=True)

    for i, day in enumerate(month):
        if not day:
            actual_date = current_date + timedelta(days=i - index)
            month[i] = Day(actual_date, is_today=False)

    return month
