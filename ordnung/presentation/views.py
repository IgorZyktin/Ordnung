# -*- coding: utf-8 -*-

"""Regular views.
"""

from starlette.requests import Request

# from controller.date_and_time import form_month, extract_date
# from controller.records import get_records, get_or_create_record
from starlette.responses import HTMLResponse, RedirectResponse
# from view.rendering import templates, get_day_names, get_offset_links, translate

from ordnung.core.date_and_time import today
from ordnung.presentation.rendering import render_template, extract_date


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
    return render_template("month.html", context)


# # @requires('authenticated')
# async def show_day(request: Request):
#     """Single day navigation.
#     """
#     chosen_date_str, chosen_date = extract_date(request)
#     namespace = request.user.namespace
#     records = get_records(chosen_date, offset=0)
#     day_records = records[chosen_date_str]
#
#     context = {
#         'request': request,
#         'header': translate(namespace, 'generic', '$day') + f' ({chosen_date_str})',
#         'chosen_date': chosen_date,
#         'chosen_date_str': chosen_date_str,
#         'records': day_records,
#         **request.state.context_extensions,
#     }
#     return templates.TemplateResponse('show_day.html', context)
#
#
# # @requires('authenticated')
# async def show_record(request: Request):
#     """Single record modification or creation.
#     """
#     chosen_date_str, chosen_date = extract_date(request)
#     record_id = request.path_params.get('record_id')
#     record, sub_context = get_or_create_record(record_id, chosen_date_str, request.user)
#
#     context = {
#         'request': request,
#         'creator_name': request.user.name,
#         'chosen_date': chosen_date,
#         'chosen_date_str': chosen_date_str,
#         'record': record,
#         **sub_context,
#         **request.state.context_extensions,
#     }
#     return templates.TemplateResponse('show_record.html', context)


async def index(request: Request) -> RedirectResponse:
    """Starting page.
    """
    if request.user.is_authenticated:
        url = request.url_for("show_month", at_date=str(today()))
        return RedirectResponse(url)

    url = request.url_for('login')
    return RedirectResponse(url)


async def register(request: Request):
    """Register page.
    """
    # FIXME
    url = request.url_for("index")
    return RedirectResponse(url)


async def password_restore(request: Request):
    """Password restore page.
    """
    # FIXME
    url = request.url_for("index")
    return RedirectResponse(url)


async def login(request: Request) -> HTMLResponse:
    """Login page.
    """
    context = {
        'request': request
    }
    return render_template("login.html", context)


async def logout(request: Request):
    """Logout page.
    """
    # FIXME
    url = request.url_for("index")
    return RedirectResponse(url)
