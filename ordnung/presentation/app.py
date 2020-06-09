# -*- coding: utf-8 -*-

"""Main app instance is here.
"""

from loguru import logger
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from ordnung import settings
from ordnung.presentation.backends import OrdnungAuthBackend
from ordnung.presentation.middleware import (
    ContextExtensionMiddleware, AuthMiddleware
)
from ordnung.presentation.routes import routes


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

app = Starlette(
    routes=routes,
    on_startup=[startup],
    middleware=middleware,
    debug=settings.DEBUG
)
