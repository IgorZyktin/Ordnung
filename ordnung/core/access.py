from datetime import datetime, date, timedelta
from typing import Tuple, List, Dict

from ordnung.core import core_settings


def form_day(chosen_date: date, lexis) -> dict:
    """Form description for a single day.
    """
    today = datetime.today().date()
    weekday = chosen_date.weekday()
    new_day = {
        'target_date': str(chosen_date),
        'number': chosen_date.day,
        'weekday': weekday,
        'month': lexis[f'month_{chosen_date.month}_'],
        'is_today': chosen_date == today,
        'is_weekend': weekday in core_settings.WEEKENDS,
    }
    return new_day


def form_month(chosen_date: date, lexis) -> List[dict]:
    """Form main table.

    Example output (shortened):
    [
        {'target_date': '2020-04-20', 'number': 20, 'weekday': 0,
        'month': '4', 'is_today': False, 'is_weekend': False},
        ...,
        {'target_date': '2020-05-24', 'number': 24, 'weekday': 6,
        'month': '5', 'is_today': False, 'is_weekend': True}
    ]
    """
    weekday_index = chosen_date.weekday()
    index = core_settings.WEEK_LENGTH + core_settings.WEEK_LENGTH + weekday_index

    month: List[dict] = [{}] * core_settings.WEEK_LENGTH * core_settings.WEEKS_IN_MONTH
    month[index] = form_day(chosen_date, lexis)

    for i, day in enumerate(month):
        if not day:
            actual_date = chosen_date + timedelta(days=i - index)
            month[i] = form_day(actual_date, lexis)

    return month


def get_offset_dates(chosen_date: date) -> Dict[str, date]:
    """Calculate target dates that we will jump onto in case user will click step/leap forward/back.

    leap_back   step_back   today   step_forward    leap_forward
        │          │          │          │               │       Default parameters:
        │          │          │          │               └────── today + 21 day
        │          │          │          └────────────────────── today + 7 days
        │          │          └───────────────────────────────── today
        │          └──────────────────────────────────────────── today - 7 days
        └─────────────────────────────────────────────────────── today - 21 day

    Example output:
        {
            'leap_back': date(2020, 4, 12),
            'step_back': date(2020, 4, 26),
            'step_forward': date(2020, 5, 10),
            'leap_forward': date(2020, 5, 24),
        }
    """
    return {
        'leap_back': chosen_date - timedelta(days=core_settings.LEAP_SIZE),
        'step_back': chosen_date - timedelta(days=core_settings.STEP_SIZE),
        'step_forward': chosen_date + timedelta(days=core_settings.STEP_SIZE),
        'leap_forward': chosen_date + timedelta(days=core_settings.LEAP_SIZE),
    }
