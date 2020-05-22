# -*- coding: utf-8 -*-

"""Tools, related to different languages processing.
"""
from datetime import date
from functools import lru_cache
from typing import Optional, List, Dict, Tuple

from ordnung.core import core_settings
from ordnung.core.vocabulary import get_vocabulary


def get_month_header(namespace: str, at_date: date) -> str:
    pass


def get_day_header(namespace: str, at_date: date) -> str:
    pass


def get_record_header(namespace: str, title: str) -> str:
    pass


@lru_cache
def extract_term(namespace: str, key: str) -> Optional[str]:
    """Get translation from the vocabulary, or None instead.

    >>> extract_term('RU', 'month')
    'Месяц'
    >>> extract_term('EN', 'lol')
    """
    mapping = get_vocabulary().get(namespace, {})
    term = mapping.get(key)
    return term


@lru_cache
def translate(namespace: str, key: str) -> str:
    """Search for translation in the vocabulary and substitute its value.

    >>> translate('RU', 'month')
    'Месяц'
    >>> translate('EN', 'month')
    'Month'
    >>> translate('EN', 'lol')
    '???'
    """
    term = extract_term(namespace, key)

    if term is None:
        term = extract_term(core_settings.DEFAULT_NAMESPACE, key)

    return term or core_settings.TERM_PLACEHOLDER


def make_lexis(namespace: str, words: List[str]) -> Dict[str, str]:
    lexis = {}
    for word in words:
        lexis[word] = translate(namespace, word)
    return lexis


def get_day_names(namespace: str) -> List[Tuple[str, str]]:
    """Get list of weekday names in user namespace.

    >>> get_day_names('RU')[:3]
    [('Понедельник', 'ПН'), ('Вторник', 'ВТ'), ('Среда', 'СР')]
    >>> get_day_names('EN')[:3]
    [('Monday', 'MON'), ('Tuesday', 'TUE'), ('Wednesday', 'WED')]
    """
    numbers = range(1, 8)
    long_names = [translate(namespace, f'day_{x}') for x in numbers]
    short_names = [translate(namespace, f'day_{x}_short') for x in numbers]
    output = list(zip(long_names, short_names))
    return output
