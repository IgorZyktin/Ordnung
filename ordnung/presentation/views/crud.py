# -*- coding: utf-8 -*-

"""Views.
"""

from starlette.requests import Request
from starlette.responses import RedirectResponse

from ordnung.presentation.access import (
    get_date, get_gettext, get_errors, get_lang
)
from ordnung.presentation.rendering import render_template
from ordnung.presentation.views.tools import (
    make_goal_creation_form, make_new_goal_from_form,
    make_goal_update_form, apply_update_on_goal
)
from ordnung.storage.database import session
from ordnung.storage.models import Goal


async def create_goal(request: Request):
    """Create new goal.
    """
    current_date = get_date(request)
    lang = get_lang(request)
    _ = get_gettext(lang)

    form = await make_goal_creation_form(request)

    if request.method == 'POST' and form.validate():
        new_goal = await make_new_goal_from_form(form)
        session.add(new_goal)
        session.commit()
        return RedirectResponse(
            request.url_for('day', date=current_date), status_code=303
        )

    errors = await get_errors(_, form.errors)

    context = {
        'request': request,
        'header': _('Create new goal'),
        'form': form,
        'errors': errors,
        'current_date': current_date,
        'mode': 'create',
    }
    return render_template('crud_goal.html', context)


async def update_goal(request: Request):
    """Update existing goal.
    """
    current_date = get_date(request)
    last_date = request.session.get('last_date', current_date)
    lang = get_lang(request)
    _ = get_gettext(lang)

    goal_id = int(request.path_params.get('goal_id'))
    goal = session.query(Goal).filter_by(id=goal_id).first()

    if goal:
        form = await make_goal_update_form(request, goal)
    else:
        form = await make_goal_creation_form(request)

    if request.method == 'POST' and form.validate():
        await apply_update_on_goal(form, goal)
        session.add(goal)
        session.commit()
        return RedirectResponse(
            request.url_for('day', date=current_date), status_code=303
        )

    errors = await get_errors(_, form.errors)

    context = {
        'request': request,
        'header': _('Update goal'),
        'form': form,
        'errors': errors,
        'current_date': current_date,
        'mode': 'update',
        'back': _('Back to month'),
    }
    return render_template('crud_goal.html', context)
