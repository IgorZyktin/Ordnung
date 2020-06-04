# -*- coding: utf-8 -*-

"""Main app instance is here.
"""

from loguru import logger
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse

from ordnung import settings
from ordnung.presentation.backends import OrdnungAuthBackend
from ordnung.presentation.middleware import (
    ContextExtensionMiddleware, AuthMiddleware
)
from ordnung.presentation.routes import routes
from ordnung.storage.database import session


def startup():
    """Gets called on server startup.
    """
    logger.add(settings.LOGGER_FILENAME, rotation=settings.LOGGER_ROTATION)
    logger.info('Server start')


middleware = [
    Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
    Middleware(AuthMiddleware, backend=OrdnungAuthBackend()),
    Middleware(ContextExtensionMiddleware),
]


async def server_error(request, exc):
    session.rollback()
    # TODO - is it actually working?
    print('server_error handler')
    return HTMLResponse(content='fuck', status_code=exc.status_code)


exception_handlers = {
    500: server_error
}

app = Starlette(
    routes=routes,
    on_startup=[startup],
    middleware=middleware,
    exception_handlers=exception_handlers,
    debug=settings.DEBUG
)
