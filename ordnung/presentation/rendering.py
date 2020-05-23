# -*- coding: utf-8 -*-

"""Tools, related to template rendering and presentation forming.
"""
from datetime import date, datetime

from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='ordnung/presentation/templates')


def render_template(name: str, context: dict, status_code: int = 200, **kwargs):
    """Render template into HTML.

    Just a small wrapper to make it look more like Flask.

    :param status_code: HTTP status code.
    :param name: template filename (html).
    :param context: dict with required variables (including request itself).
    :return: rendered Jinja2 template.
    """
    extensions = context['request'].state.context_extensions
    context = {**context, **extensions, **kwargs}
    return templates.TemplateResponse(name, context, status_code)


def extract_date(request: Request) -> date:
    """Extract date from request arguments.

    :param request: starlette Request instance.
    :return: stdlib date object.

    Example output:
        date(2020, 5, 3)
    """
    str_at_date = request.path_params['at_date']
    at_date = datetime.strptime(str_at_date, "%Y-%m-%d").date()
    return at_date
