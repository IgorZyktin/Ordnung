# -*- coding: utf-8 -*-

"""Tools, related to different languages processing.
"""
import json
import os
from datetime import date
from pathlib import Path
from typing import Optional

from ordnung.core import core_settings
from ordnung.storage import storage_settings

try:
    path = Path().resolve() / storage_settings.VOCABULARY_FILE

    if not path.exists():
        path = Path(os.pardir).resolve() / storage_settings.VOCABULARY_FILE

    with open(str(path.resolve()), mode="r", encoding="utf-8") as file:
        VOCABULARY = json.load(file)

except FileNotFoundError:
    VOCABULARY = {}


def get_month_header(namespace: str, at_date: date) -> str:
    pass


def get_day_header(namespace: str, at_date: date) -> str:
    pass


def get_record_header(namespace: str, title: str) -> str:
    pass


def extract_term(namespace: str, field: str, value: str) -> Optional[str]:
    """Get translation from the vocabulary, or None instead.
    >>> extract_term('RU', 'generic', '$month')
    'Месяц'
    >>> extract_term('EN', 'generic', '$lol')
    """
    space = VOCABULARY.get(namespace, {})
    mapping = space.get(field, {})
    term = mapping.get(value)
    return term


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
