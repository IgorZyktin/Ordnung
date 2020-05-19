# -*- coding: utf-8 -*-

"""Regular views.
"""

from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from ordnung.core.date_and_time import today
from ordnung.core.localisation import translate
from ordnung.presentation.rendering import render_template, extract_date

HTTP_OK = 200
HTTP_UNAUTHORIZED = 401


@requires('authenticated', redirect='unauthorized')
async def show_month(request: Request):
    """Main page, navigation starts from here. Shows single month.
    """
    at_date = extract_date(request)
    #     namespace = request.user.namespace
    #
    context = {
        'request': request,
        #         'header': translate(namespace, 'generic', '$month') + f' ({chosen_date_str})',
        #         'month': form_month(chosen_date),
        #         'records': get_records(chosen_date),
        'at_date': at_date,
        #         'day_names': get_day_names(namespace),
        #         **get_offset_links(chosen_date, request),
        #         **request.state.context_extensions,
    }
    return HTMLResponse(f'month - {at_date}')
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
        return RedirectResponse(request.url_for("show_month", at_date=str(today())))
    return RedirectResponse(request.url_for('login'))


async def login(request: Request) -> HTMLResponse:
    """Login page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(request.url_for('index'))

    context = {
        'request': request,
        'header': translate(request.user.namespace, 'generic', '$login_failed'),
        'retry': translate(request.user.namespace, 'generic', '$login_retry'),
        'register': translate(request.user.namespace, 'generic', '$goto_register'),
        'restore': translate(request.user.namespace, 'generic', '$goto_restore'),
        'errors': {},
    }

    response = render_template("login.html", context, status_code=HTTP_UNAUTHORIZED)
    response.headers['WWW-Authenticate'] = 'Basic realm="ordnung"'
    return response


async def register(request: Request):
    """Register page.
    """
    errors = {}
    if request.method == 'POST':
        pass

    context = {
        'request': request,
        'header': translate(request.user.namespace, 'generic', '$register'),
        'errors': errors,
    }
    return render_template("register.html", context)


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
    return render_template("login_basic.html", context, status_code=401)


@requires('authenticated', redirect='unauthorized')
async def logout(request: Request) -> HTMLResponse:
    """Logout page.
    """
    context = {
        'request': request,
        'header': translate(request.user.namespace, 'generic', '$logout'),
        'errors': {},
    }
    return render_template("login_basic.html", context, status_code=401)
