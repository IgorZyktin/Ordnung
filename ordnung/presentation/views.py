# -*- coding: utf-8 -*-

"""Regular views.
"""
from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from ordnung.core.date_and_time import get_offset_dates, form_month
from ordnung.core.localisation import translate, get_day_names
from ordnung.presentation.access import get_lang, get_date
from ordnung.presentation.presentation_settings import HTTP_POST_REDIRECT_GET
from ordnung.presentation.rendering import render_template, extract_date
from ordnung.presentation.validation import registration_form_is_invalid
from ordnung.storage.access import register_new_user, send_verification_email


# TODO - должно быть доступно только после авторизации
# @requires('authenticated', redirect='unauthorized')
async def month(request: Request) -> HTMLResponse:
    """Main page, navigation starts from here. Shows single month.
    """
    lang = get_lang(request)
    current_date = get_date(request)
    header = translate(lang, f'month_{current_date.month}') + f' ({current_date})'

    base_url = request.url_for('month')
    leap_back, step_back, step_forward, leap_forward = get_offset_dates(current_date)

    context = {
        'request': request,
        'header': header,
        'month': form_month(current_date),
        'records': {},  # FIXME
        'tasks': [['a', 'b', 'c'], ['d', 'e', 'f']],
        'lang': lang,
        'menu_is_visible': int(request.query_params.get('menu', '0')),
        'current_date': current_date,
        'day_names': get_day_names(lang),
        'leap_back_url': f'{base_url}?date={leap_back}',
        'step_back_url': f'{base_url}?date={step_back}',
        'step_forward_url': f'{base_url}?date={step_forward}',
        'leap_forward_url': f'{base_url}?date={leap_forward}',
    }
    return render_template("month.html", context)


@requires('authenticated', redirect='unauthorized')
async def show_day(request: Request):
    """Single day navigation.
    """
    at_date = extract_date(request)
    #     chosen_date_str, chosen_date = extract_date(request)
    #     namespace = request.user.namespace
    #     records = get_records(chosen_date, offset=0)
    #     day_records = records[chosen_date_str]
    #
    context = {
        'request': request,
        #         'header': translate(namespace, 'generic', '$day') + f' ({chosen_date_str})',
        #         'chosen_date': chosen_date,
        #         'chosen_date_str': chosen_date_str,
        #         'records': day_records,
        #         **request.state.context_extensions,
    }
    return HTMLResponse(f'day - {at_date}')


#     return templates.TemplateResponse('show_day.html', context)


@requires('authenticated', redirect='unauthorized')
async def show_record(request: Request):
    """Single record modification or creation.
    """
    at_date = extract_date(request)
    #     chosen_date_str, chosen_date = extract_date(request)
    #     record_id = request.path_params.get('record_id')
    #     record, sub_context = get_or_create_record(record_id, chosen_date_str, request.user)
    #
    context = {
        'request': request,
        #         'creator_name': request.user.name,
        #         'chosen_date': chosen_date,
        #         'chosen_date_str': chosen_date_str,
        #         'record': record,
        #         **sub_context,
        #         **request.state.context_extensions,
    }
    return HTMLResponse(f'day - {at_date}')


async def index(request: Request) -> RedirectResponse:
    """Starting page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(request.url_for("month"))
    return RedirectResponse(request.url_for('login'))


async def login(request: Request) -> HTMLResponse:
    """Login page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(request.url_for('index'), status_code=HTTP_POST_REDIRECT_GET)

    context = {
        'request': request,
        'header': translate(request.user.namespace, 'generic', '$login_failed'),
        'retry': translate(request.user.namespace, 'generic', '$login_retry'),
        'register': translate(request.user.namespace, 'generic', '$goto_register'),
        'restore': translate(request.user.namespace, 'generic', '$goto_restore'),
        'errors': {},
    }

    response = render_template("login.html", context, status_code=401)
    response.headers['WWW-Authenticate'] = 'Basic realm="ordnung"'
    return response


async def register(request: Request):
    """Register page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(request.url_for('index'))

    errors = {}
    form = await request.form()

    if request.method == 'POST':
        if not (errors := registration_form_is_invalid(form)):
            register_new_user('s')
            send_verification_email()
            return RedirectResponse(request.url_for('register_confirm'),
                                    status_code=HTTP_POST_REDIRECT_GET)

    context = {
        'request': request,
        'header': translate(request.user.namespace, 'generic', '$register'),
        'entered_name': form.get('username', ''),
        'entered_login': form.get('login', ''),
        'entered_email': form.get('email', ''),
        'errors': errors,
    }
    return render_template("register.html", context)


async def register_confirm(request: Request):
    """Register page. Message about e-mail confirmation.
    """
    if request.user.is_authenticated:
        return RedirectResponse(request.url_for('index'))

    email = request.user.email

    context = {
        'request': request,
        'header': translate(request.user.namespace, 'generic', '$register'),
        'email': email,
        'errors': {},
    }
    return render_template("register_confirm.html", context)


async def restore_start(request: Request):
    """Password restore page.
    """
    errors = {}
    if request.method == 'POST':
        pass

    context = {
        'request': request,
        'header': translate(request.user.namespace, 'generic', '$restore_start'),
        'errors': errors,
    }
    return render_template("restore_start.html", context)


async def restore_form(request: Request):
    """Password restore page (actual form).
    """
    errors = {}
    if request.method == 'POST':
        pass

    context = {
        'request': request,
        'header': translate(request.user.namespace, 'generic', '$restore_prove'),
        'errors': errors,
    }
    return render_template("restore_main.html", context)


async def unauthorized(request: Request) -> HTMLResponse:
    """When user is not yet authorised but tries to get something.
    """
    context = {
        'request': request,
        'header': translate(request.user.namespace, 'generic', '$unauthorized'),
        'errors': {},
    }
    return render_template("unauthorized.html", context, status_code=403)


@requires('authenticated', redirect='unauthorized')
async def logout(request: Request) -> HTMLResponse:
    """Logout page.
    """
    context = {
        'request': request,
        'header': translate(request.user.namespace, 'generic', '$logout'),
        'errors': {},
    }
    return render_template("logout.html", context, status_code=401)
