# -*- coding: utf-8 -*-

"""Core language processing.
"""
from typing import List, Tuple

from ordnung import settings
from ordnung.core.vocabulary import (
    get_static_vocabulary, get_dynamic_vocabulary
)


def gettext(lang: str, sentence: str) -> str:
    """Translate message and return it as a string.

    Similar to Django gettext, but without session middleware,
    so we have to pass locale explicitly.

    >>> gettext('RU', 'January')
    'Январь'
    """
    if lang == settings.DEFAULT_LANG:
        translation = sentence

    elif (vocabulary := get_static_vocabulary().get(lang)) is None:
        translation = sentence

    elif (translation := vocabulary.get(sentence)) is None:
        translation = sentence

    return translation


def translate(lang: str, key: str) -> str:
    """Search for translation in the vocabulary and substitute its value.

    >>> translate('RU', 'month_1')
    'Январь'
    >>> translate('EN', 'month_1')
    'January'
    >>> translate('EN', 'lol')
    '???'
    """
    if (vocabulary := get_dynamic_vocabulary().get(lang)) is None:
        vocabulary = get_dynamic_vocabulary().get(settings.DEFAULT_LANG)

    while (translation := vocabulary.get(key)) is None:
        if key.endswith('_'):
            key = key[:-1]
        else:
            translation = settings.DEFAULT_PLACEHOLDER
            break

    return translation


def get_day_names(lang: str) -> List[Tuple[str, str]]:
    """Get list of weekday names in user lang.

    >>> get_day_names('RU')[:3]
    [('Понедельник', 'ПН'), ('Вторник', 'ВТ'), ('Среда', 'СР')]
    >>> get_day_names('EN')[:3]
    [('Monday', 'MON'), ('Tuesday', 'TUE'), ('Wednesday', 'WED')]
    """
    numbers = range(1, 8)
    long_names = [translate(lang, f'day_{x}') for x in numbers]
    short_names = [translate(lang, f'day_{x}_short') for x in numbers]
    return list(zip(long_names, short_names))
