# -*- coding: utf-8 -*-

"""Tools, related to different languages processing.
"""
from datetime import date
from functools import lru_cache
from typing import Optional

from ordnung.core import core_settings
from ordnung.storage.access import get_vocabulary


def get_month_header(namespace: str, at_date: date) -> str:
    pass


def get_day_header(namespace: str, at_date: date) -> str:
    pass


def get_record_header(namespace: str, title: str) -> str:
    pass


@lru_cache
def extract_term(namespace: str, field: str, value: str) -> Optional[str]:
    """Get translation from the vocabulary, or None instead.

    >>> extract_term('RU', 'generic', '$month')
    'Месяц'
    >>> extract_term('EN', 'generic', '$lol')
    """
    space = get_vocabulary().get(namespace, {})
    mapping = space.get(field, {})
    term = mapping.get(value)
    return term


@lru_cache
def translate(namespace: str, field: str, value: str) -> str:
    """Search for translation in the vocabulary and substitute its value.

    >>> translate('RU', 'generic', '$month')
    'Месяц'
    >>> translate('EN', 'generic', '$month')
    'Month'
    >>> translate('EN', 'generic', '$lol')
    '???'
    """
    term = extract_term(namespace, field, value)

    if term is None:
        term = extract_term(core_settings.DEFAULT_NAMESPACE, field, value)

    return term or core_settings.TERM_PLACEHOLDER
