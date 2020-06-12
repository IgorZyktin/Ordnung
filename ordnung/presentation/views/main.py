# -*- coding: utf-8 -*-

"""Views.
"""

from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import HTMLResponse

from ordnung.core.date_and_time import get_offset_dates, get_month, get_day
from ordnung.core.localisation import get_day_names
from ordnung.presentation.access import get_date, get_translate, get_lang
from ordnung.presentation.rendering import render_template


# @requires('authenticated', redirect='unauthorized')
async def month(request: Request) -> HTMLResponse:
    """Main page, navigation starts from here. Shows single month.
    """
    current_date = await get_date(request)
    tr = get_translate(get_lang(request))
    url_for = request.url_for

    (leap_back, step_back,
     step_forward, leap_forward) = get_offset_dates(current_date)

    all_days_in_month = get_month(current_date)

    goal_sections = {
        str(current_date): all_days_in_month[str(current_date)].goals()
    }

    context = {
        'request': request,
        'header': tr(f'month_{current_date.month}') + f' ({current_date})',
        'month': all_days_in_month,
        'goal_sections': [],
        'menu_is_visible': 0,  # FIXME
        'current_date': current_date,
        'day_names': get_day_names(get_lang(request)),
        'leap_back_url': url_for('month', date=leap_back),
        'step_back_url': url_for('month', date=step_back),
        'step_forward_url': url_for('month', date=step_forward),
        'leap_forward_url': url_for('month', date=leap_forward),
    }
    return render_template('month.html', context)


# @requires('authenticated', redirect='unauthorized')
async def day(request: Request):
    """Single day navigation.
    """
    current_date = await get_date(request)
    _ = get_translate(get_lang(request))

    curr_day = get_day(current_date, is_today=True)

    context = {
        'request': request,
        'header': _(f'month_{current_date.month}') + f' ({current_date})',
        'current_date': current_date,
        'goals': curr_day.goals()
    }
    return render_template("day.html", context)
