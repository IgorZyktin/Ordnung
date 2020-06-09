# -*- coding: utf-8 -*-

"""Views helping tools.
"""
from datetime import datetime

from starlette.requests import Request

from ordnung.core.access import get_now
from ordnung.core.date_and_time import get_time_variants
from ordnung.core.localisation import get_user_group_names, \
    get_persistence_names, get_statuses_names
from ordnung.presentation.access import get_lang, get_date
from ordnung.presentation.forms import GoalForm
from ordnung.storage.models import Goal


async def make_goal_creation_form(request: Request) -> GoalForm:
    """Make form for the new goal.
    """
    lang = get_lang(request)
    current_date = get_date(request)

    form = await request.form()
    form = GoalForm(formdata=form,
                    lang=lang,
                    meta={'csrf_context': request.session})

    form.user_id.data = request.user.id
    form.group.choices = get_user_group_names(request.user.groups)
    form.target_date.data = current_date
    form.persistence.choices = get_persistence_names(lang)
    form.target_time.choices = get_time_variants()
    form.status.choices = get_statuses_names(lang)

    form.metric_name.disabled = True
    form.metric_objective.disabled = True
    form.metric_step.disabled = True
    return form


async def make_goal_update_form(request: Request, goal: Goal) -> GoalForm:
    """Make form for an existing goal.
    """
    lang = get_lang(request)
    current_date = get_date(request)

    form = await request.form()
    form = GoalForm(formdata=form,
                    lang=lang,
                    obj=goal,
                    meta={'csrf_context': request.session})

    # form.id.data = goal.id
    # form.title.data = goal.title
    # form.description.data = goal.description

    form.group.choices = get_user_group_names(request.user.groups)
    # form.target_date.data = goal.target_date
    form.persistence.choices = get_persistence_names(lang)
    form.target_time.choices = get_time_variants()
    form.status.choices = get_statuses_names(lang)
    # form.created.data = request_form.get('created', goal.created)

    # form.metric_name.data = request_form.get('metric_name', goal.metric_name)
    # form.metric_objective.data = request_form.get('metric_objective',
    #                                               goal.metric_objective)
    # form.metric_step.data = request_form.get('metric_step', goal.metric_step)

    # form.metric_name.disabled = True
    # form.metric_objective.disabled = True
    # form.metric_step.disabled = True
    return form


async def make_new_goal_from_form(form: GoalForm) -> Goal:
    """Make new Goal instance from form.
    """
    new_goal = Goal(
        user_id=int(form.user_id.data),
        group_id=int(form.group.data[0]),
        persistence_id=int(form.persistence.data[0]),
        created=get_now(),
        last_edit=get_now(),
        title=form.title.data,
        description=form.description.data,
        target_date=form.target_date.data,
        start_time=get_now(),
    )
    return new_goal


async def apply_update_on_goal(form: GoalForm, goal: Goal):
    print('apply_update_on_goal', vars(form))
    print(form.title)
    print(form.title.data)
    print('---')
    goal.group_id = int(form.group.data[0])
    goal.persistence_id = int(form.persistence.data[0])
    goal.last_edit = get_now()
    goal.title = form.title.data
    goal.description = form.description.data
    goal.target_date = form.target_date.data

    if form.start_time.data:
        goal.start_time = datetime.strptime(form.start_time.data,
                                            "%Y-%m-%d").astimezone()
