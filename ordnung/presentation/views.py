# -*- coding: utf-8 -*-

"""Regular views.
"""
from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from ordnung import settings
from ordnung.core.records import organize_records
from ordnung.core.date_and_time import get_offset_dates, form_month
from ordnung.core.localisation import translate, get_day_names, gettext
from ordnung.presentation.access import get_date, get_lang
from ordnung.presentation.rendering import render_template, extract_date
from ordnung.storage.database import get_records

HTTP_OK = 200
HTTP_POST_REDIRECT_GET = 303
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403


@requires('authenticated', redirect='unauthorized')
async def month(request: Request) -> HTMLResponse:
    """Main page, navigation starts from here. Shows single month.
    """
    lang = get_lang(request)
    current_date = get_date(request)
    header = translate(lang, f'month_{current_date.month}') + f' ({current_date})'
    leap_back, step_back, step_forward, leap_forward = get_offset_dates(current_date)

    all_records = get_records(current_date, settings.MONTH_OFFSET)
    records = organize_records(all_records)

    context = {
        'request': request,
        'header': header,
        'month': form_month(current_date),
        'records': records,
        'tasks': [['a', 'b', 'c'], ['d', 'e', 'f']],  # FIXME
        'lang': lang,
        'menu_is_visible': int(request.query_params.get('menu', '0')),
        'current_date': current_date,
        'day_names': get_day_names(lang),
        'leap_back_url': f'/month?date={leap_back}',
        'step_back_url': f'/month?date={step_back}',
        'step_forward_url': f'/month?date={step_forward}',
        'leap_forward_url': f'/month?date={leap_forward}',
    }
    print(context['records'])
    return render_template("month.html", context)


@requires('authenticated', redirect='unauthorized')
async def day(request: Request):
    """Single day navigation.
    """
    lang = get_lang(request)
    current_date = get_date(request)
    header = translate(lang, f'month_{current_date.month}') + f' ({current_date})'

    context = {
        'request': request,
        'header': header,
        'lang': lang,
        'current_date': current_date,
        'month_url': f'/month?date={current_date}',
        'records': ['1', '2']
    }
    return render_template("day.html", context)


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
        return RedirectResponse(request.url_for('month'))
    return RedirectResponse(request.url_for('login'))


async def login(request: Request) -> HTMLResponse:
    """Login page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(request.url_for('index'), status_code=HTTP_POST_REDIRECT_GET)

    lang = get_lang(request)

    context = {
        'request': request,
        'lang': lang,
        'header': gettext(lang, "You may gain access only after login"),
        'retry': translate(lang, "Try log in once again"),
        'register': translate(lang, "Register"),
        'restore': translate(lang, "Restore password"),
        'errors': {},
    }
    return render_template("login.html", context, HTTP_UNAUTHORIZED, {"WWW-Authenticate": "Basic"})


async def register(request: Request):
    """Register page.
    """
    # if request.user.is_authenticated:
    #     return RedirectResponse(request.url_for('index'))
    #
    # errors = {}
    # form = await request.form()
    #
    # if request.method == 'POST':
    #     if not (errors := registration_form_is_invalid(form)):
    #         register_new_user('s')
    #         send_verification_email()
    #         return RedirectResponse(request.url_for('register_confirm'),
    #                                 status_code=HTTP_POST_REDIRECT_GET)
    #
    # context = {
    #     'request': request,
    #     'header': translate(request.user.namespace, 'generic', '$register'),
    #     'entered_name': form.get('username', ''),
    #     'entered_login': form.get('login', ''),
    #     'entered_email': form.get('email', ''),
    #     'errors': errors,
    # }
    # return render_template("register.html", context)
    raise


# TODO
async def register_confirm(request: Request):
    """Register page. Message about e-mail confirmation.
    """
    # if request.user.is_authenticated:
    #     return RedirectResponse(request.url_for('index'))
    #
    # email = request.user.email
    #
    # context = {
    #     'request': request,
    #     'header': translate(request.user.namespace, 'generic', '$register'),
    #     'email': email,
    #     'errors': {},
    # }
    # return render_template("register_confirm.html", context)
    raise


# TODO
async def restore_start(request: Request):
    """Password restore page.
    """
    # errors = {}
    # if request.method == 'POST':
    #     pass
    #
    # context = {
    #     'request': request,
    #     'header': translate(request.user.namespace, 'generic', '$restore_start'),
    #     'errors': errors,
    # }
    # return render_template("restore_start.html", context)
    raise


# TODO
async def restore_form(request: Request):
    """Password restore page (actual form).
    """
    # errors = {}
    # if request.method == 'POST':
    #     pass
    #
    # context = {
    #     'request': request,
    #     'header': translate(request.user.namespace, 'generic', '$restore_prove'),
    #     'errors': errors,
    # }
    # return render_template("restore_main.html", context)
    raise


async def unauthorized(request: Request) -> HTMLResponse:
    """When user is not yet authorised but tries to get something.
    """
    lang = get_lang(request)

    context = {
        'request': request,
        'lang': lang,
        'header': gettext(lang, "You have no access to this resource"),
        'errors': {},
    }
    return render_template("unauthorized.html", context, status_code=HTTP_FORBIDDEN)


@requires('authenticated', redirect='unauthorized')
async def logout(request: Request) -> HTMLResponse:
    """Logout page.
    """
    lang = get_lang(request)

    context = {
        'request': request,
        'lang': lang,
        'header': gettext(lang, "You have been successfully logged out"),
        'errors': {},
    }
    return render_template("logout.html", context, status_code=HTTP_UNAUTHORIZED)
