# -*- coding: utf-8 -*-

"""Form checking.
"""
import re
from typing import Dict

from starlette.datastructures import FormData, QueryParams
from werkzeug.security import check_password_hash

from ordnung.storage.access import get_user_by_login


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


def registration_form_is_invalid(form: FormData) -> Dict[str, str]:
    if 'username' not in form:
        return {'no_name': 'Для регистрации необходимо указать имя.'}

    if 'login' not in form:
        return {'no_login': 'Для регистрации необходимо указать логин.'}

    if len(form['login']) < 3:
        return {'short_login': 'Слишком короткий логин.'}

    if 'email' not in form:
        return {'no_email': 'Для входа необходимо указать e-mail.'}

    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", form['email']):
        return {'wrong_email': 'Неправильно указан e-mail.'}

    if 'password' not in form:
        return {'no_password': 'Для входа необходимо указать пароль.'}

    if 'password_repeat' not in form:
        return {'no_password_repeat': 'Для входа необходимо повторить пароль.'}

    if len(form['password']) < 5:
        return {'short_password': 'Слишком короткий пароль.'}

    if form['password'] != form['password_repeat']:
        return {'passwords_dont_match': 'Введенные пароли не совпадают друг с другом.'}

    return {}
