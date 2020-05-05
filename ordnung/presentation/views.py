# -*- coding: utf-8 -*-

"""Regular views.
"""
import json
from base64 import b64encode

from starlette.authentication import requires
from starlette.requests import Request

# from controller.date_and_time import form_month, extract_date
# from controller.records import get_records, get_or_create_record
from starlette.responses import HTMLResponse, RedirectResponse
# from view.rendering import templates, get_day_names, get_offset_links, translate

from ordnung.core.date_and_time import today
from ordnung.presentation.rendering import render_template, extract_date
from ordnung.presentation.validation import login_form_is_invalid, extract_errors, format_errors

HTTP_OK = 200
HTTP_POST_REDIRECT_GET = 303


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
#     return templates.TemplateResponse('show_record.html', context)


async def index(request: Request) -> RedirectResponse:
    """Starting page.
    """
    if request.user.is_authenticated:
        url = request.url_for("show_month", at_date=str(today()))
        return RedirectResponse(url)

    url = request.url_for('login')
    return RedirectResponse(url)


async def login(request: Request) -> HTMLResponse:
    """Login page.
    """
    user = request.user

    print(request, f'{user.is_authenticated=}')
    if user.is_authenticated:
        url = request.url_for("show_month", at_date=str(today()))
        return RedirectResponse(url, status_code=HTTP_POST_REDIRECT_GET)

    login_value = request.query_params.get('login', '')
    password_value = request.query_params.get('password', '')

    context = {
        'request': request,
        'login': login_value,
        'password': password_value,
        'errors': extract_errors(request.query_params)
    }

    if request.method == 'POST':
        form = await request.form()
        action = form.get('action')

        if action == 'register':
            url = request.url_for('register')
            return RedirectResponse(url, status_code=HTTP_POST_REDIRECT_GET)

        elif action == 'restore':
            url = request.url_for('restore')
            return RedirectResponse(url, status_code=HTTP_POST_REDIRECT_GET)

        elif action == 'login':
            errors = login_form_is_invalid(form)

            if not errors:
                login_text = form.get('login')
                password_text = form.get('password')
                body = b64encode(f"{login_text}:{password_text}".encode('utf-8')).decode("ascii")
                url = request.url_for("show_month", at_date=str(today()))
                response = RedirectResponse(url, status_code=HTTP_POST_REDIRECT_GET)
                response.set_cookie(
                    "Authorization",
                    value=f"Basic {body}",
                    httponly=False,
                    max_age=1800,
                    expires=1800,
                )
                return response

            login_value = form.get('login')
            password_value = form.get('password')
            query_string = '&'.join([
                format_errors(errors),
                f'login={login_value}',
                f'password={password_value}'
            ])
            url = request.url_for('login') + '?' + query_string
            return RedirectResponse(url, status_code=HTTP_POST_REDIRECT_GET)

    return render_template("login.html", context, status_code=401)


async def register(request: Request):
    """Register page.
    """
    return HTMLResponse('register')


async def restore(request: Request):
    """Password restore page.
    """
    return HTMLResponse('password_restore')


async def unauthorized(request: Request):
    """
    """
    return HTMLResponse('unauthorized')


@requires('authenticated', redirect='unauthorized')
async def logout(request: Request):
    """Logout page.
    """
    # FIXME
    print(request.cookies)
    response = HTMLResponse('logout okay')
    response.set_cookie(
        "Authorization",
        value=f"Basic " + b64encode(b"user:password").decode("ascii"),
        httponly=False,
        max_age=1800,
        expires=1800,
    )
    return response
