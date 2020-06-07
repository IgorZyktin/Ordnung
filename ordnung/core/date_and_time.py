# -*- coding: utf-8 -*-

"""Tools, related to time operations.
"""
from datetime import date, timedelta
from typing import Tuple, List, Dict, Generator

from ordnung import settings
from ordnung.core.access import get_today


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

    def goals(self):
        """Enlist goals for this day.
        """
        return [1, 2]


class Month:
    """Container for Days.
    """

    def __init__(self, current_date: date) -> None:
        """Initialize instance.
        """
        self.origin_date = current_date
        self.current_date = str(current_date)
        self.days_list: List[Day] = []
        self.days_dict: Dict[str, Day] = {}
        self.today_index = 0

    def __repr__(self) -> str:
        """Textual representation.
        """
        return (f'{type(self).__name__}'
                f'<{self.days_list[0:1]}..{self.days_list[-2:-1]}>')

    def add_day(self, new_day: Day):
        """Put day in month. Created to fill days_dict.
        """
        position = len(self.days_list)
        self.days_list.append(new_day)
        self.days_dict[new_day.date] = new_day

        if new_day.is_today:
            self.today_index = position

    def weeks(self) -> Generator[List[Day], None, None]:
        """Iterate over weeks.
        """
        top_level = settings.MONTH_LENGTH + 1 - settings.WEEK_LENGTH
        for i in range(0, top_level, settings.WEEK_LENGTH):
            sector = slice(i, i + settings.WEEK_LENGTH)
            yield self.days_list[sector]


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


def get_month(current_date: date) -> Month:
    """Form contents for the main table.

    Example output:
        Month(
            Day(2020-05-04),
            Day(2020-05-05),
            Day(2020-05-06),
            Day(2020-05-07),
            ...
        )
    """
    weekday = current_date.weekday()
    index = settings.WEEK_LENGTH * 2 + weekday
    days_total = settings.WEEK_LENGTH * settings.WEEKS_IN_MONTH

    month = Month(current_date)
    for day_number in range(days_total):
        actual_date = current_date + timedelta(days=day_number - index)
        new_day = Day(actual_date, is_today=day_number == index)
        month.add_day(new_day)

    return month

x = Month(get_today())
print(x)
print(x.weeks())