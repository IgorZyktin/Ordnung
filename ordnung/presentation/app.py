# -*- coding: utf-8 -*-

"""Main app instance is here.
"""
from loguru import logger
from starlette.applications import Starlette
from starlette.middleware import Middleware

from ordnung.presentation import presentation_settings
from ordnung.presentation.backends import OrdnungAuthBackend
from ordnung.presentation.middleware import AuthMiddleware, ContextExtensionMiddleware
from ordnung.presentation.routes import routes
from ordnung.storage import storage_settings
from ordnung.storage.database import init_db


def startup():
    """Gets called on server startup.
    """
    init_db()
    logger.add(storage_settings.LOGGER_FILENAME, rotation=storage_settings.LOGGER_ROTATION)
    logger.info('Server start')


middleware = [
    Middleware(AuthMiddleware, backend=OrdnungAuthBackend()),
    Middleware(ContextExtensionMiddleware),
]

app = Starlette(
    routes=routes,
    on_startup=[startup],
    middleware=middleware,
    debug=presentation_settings.DEBUG
)
