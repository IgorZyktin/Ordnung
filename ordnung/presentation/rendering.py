# -*- coding: utf-8 -*-

"""Tools, related to template rendering and presentation forming.
"""
from datetime import date, datetime

from starlette.requests import Request
from starlette.templating import Jinja2Templates

from ordnung.presentation.access import url_for

templates = Jinja2Templates(directory='ordnung/presentation/templates')


def render_template(name: str, context: dict, status_code: int = 200,
                    headers: dict = None, **kwargs):
    """Render template into HTML.

    Just a small wrapper to make it look more like Flask.
    """
    headers = headers or {}
    extensions = context['request'].state.context_extensions
    context = {**extensions, **context, **kwargs}
    context['index_url'] = url_for(context['request'], 'index')
    return templates.TemplateResponse(name, context, status_code, headers)


def extract_date(request: Request) -> date:
    """Extract date from request arguments.

    Example output:
        date(2020, 5, 3)
    """
    str_at_date = request.path_params['at_date']
    at_date = datetime.strptime(str_at_date, "%Y-%m-%d").date()
    return at_date
