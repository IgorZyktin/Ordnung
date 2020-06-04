# -*- coding: utf-8 -*-

"""Tools, related to template rendering and presentation forming.
"""

from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='ordnung/presentation/templates')


def render_template(name: str, context: dict, status_code: int = 200,
                    headers: dict = None, **kwargs):
    """Render template into HTML.

    Just a small wrapper to make it look more like Flask.
    """
    headers = headers or {}
    extensions = context['request'].state.context_extensions
    context = {**extensions, **context, **kwargs}
    context['index_url'] = context['request'].url_for('index')
    return templates.TemplateResponse(name, context, status_code, headers)
