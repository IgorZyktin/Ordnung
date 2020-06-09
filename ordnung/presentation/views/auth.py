# -*- coding: utf-8 -*-

"""Views.
"""
from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse

from ordnung.presentation.access import get_gettext, get_lang
from ordnung.presentation.rendering import render_template


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
        return RedirectResponse(request.url_for('index'))

    _ = get_gettext(get_lang(request))

    context = {
        'request': request,
        'header': _('You could get access only after login'),
        'retry': _('Try log in once again'),
        'register': _('Register'),
        'restore': _('Restore password'),
    }
    return render_template(
        "login.html", context, status_code=401,
        headers={"WWW-Authenticate": 'Basic realm="Ordnung"'}
    )


async def unauthorized(request: Request) -> HTMLResponse:
    """When user is not yet authorised but tries to get something.
    """
    _ = get_gettext(get_lang(request))

    context = {
        'request': request,
        'header': _('You have no access to this resource'),
        'retry': _('To the start page'),
    }
    return render_template('unauthorized.html', context, status_code=403)


@requires('authenticated', redirect='unauthorized')
async def logout(request: Request) -> HTMLResponse:
    """Logout page.
    """
    _ = get_gettext(get_lang(request))

    context = {
        'request': request,
        'header': _('You have been successfully logged out'),
        'retry': _('To the start page'),
    }
    return render_template('login_note.html', context, status_code=401)
