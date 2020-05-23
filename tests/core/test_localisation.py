# -*- coding: utf-8 -*-

"""Core language processing.
"""
import pytest

from ordnung.core import core_settings
from ordnung.core.localisation import get_day_names, translate, gettext


@pytest.fixture()
def ref_day_names(lang):
    return {
        'EN': [('Monday', 'MON'),
               ('Tuesday', 'TUE'),
               ('Wednesday', 'WED'),
               ('Thursday', 'THU'),
               ('Friday', 'FRI'),
               ('Saturday', 'SAT'),
               ('Sunday', 'SUN')],

        'RU': [('Понедельник', 'ПН'),
               ('Вторник', 'ВТ'),
               ('Среда', 'СР'),
               ('Четверг', 'ЧТ'),
               ('Пятница', 'ПТ'),
               ('Суббота', 'СБ'),
               ('Воскресенье', 'ВС')],
    }[lang]


@pytest.mark.parametrize('lang,ref_day_names', [
    ('EN', 'EN'),
    ('RU', 'RU')
], indirect=['ref_day_names'])
def test_get_day_names(lang, ref_day_names):
    assert get_day_names(lang) == ref_day_names


def test_translate():
    assert translate('RU', 'month_1') == 'январь'
    assert translate('RU', 'month_1_') == 'января'
    assert translate('RU', 'month_1_____') == 'января'
    assert translate('JP', 'month_1') == 'january'
    assert translate('JP', 'something') == core_settings.DEFAULT_PLACEHOLDER


def test_gettext():
    assert gettext('RU', 'month') == 'месяц'
    assert gettext('JP', 'month') == 'month'
    assert gettext('RU', 'wtf') == 'wtf'
    assert gettext('EN', 'wtf') == 'wtf'
