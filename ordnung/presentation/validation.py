# -*- coding: utf-8 -*-

"""Form checking.
"""
from typing import Dict

from starlette.datastructures import FormData, QueryParams

from ordnung.presentation.backends import BaseUser
from ordnung.storage.access import get_existing_logins, get_user_by_login
from werkzeug.security import generate_password_hash, check_password_hash


def extract_errors(params: QueryParams) -> dict:
    output = {}
    for key, value in params.items():
        if key.startswith('error_'):
            output[key[6:]] = value
    return output


def format_errors(errors: dict) -> str:
    output = ''
    elements = []
    for key, value in errors.items():
        elements.append(f'error_{key}={value}')
        output = '&'.join(elements)
    return output


def login_form_is_invalid(form: FormData) -> Dict[str, str]:
    if not (login := form.get('username')):
        return {'no_login': 'Для входа необходимо указать логин.'}

    user = get_user_by_login(login)
    if user is None:
        return {'unknown_login': 'В базе нет пользователя с таким логином.'}

    if not (password := form.get('password')):
        return {'no_password': 'Для входа необходимо указать пароль.'}

    if not check_password_hash(user.password, password):
        return {'wrong_password': 'Пароль указан неправильно.'}

    return {}
