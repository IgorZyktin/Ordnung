# -*- coding: utf-8 -*-

"""Middleware classes.
"""

from starlette.authentication import AuthenticationError, AuthCredentials
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import HTTPConnection
from starlette.types import Scope, Receive, Send

from ordnung.core.localisation import translate, gettext
from ordnung.presentation.access import get_lang
from ordnung.presentation.backends import UnauthenticatedUser


class AuthMiddleware(AuthenticationMiddleware):
    """Handles user authorisation.
    """

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)
        try:
            auth_result = await self.backend.authenticate(conn)
        except AuthenticationError as exc:
            response = self.on_error(conn, exc)
            if scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1000})
            else:
                await response(scope, receive, send)
            return

        if auth_result is None:
            auth_result = AuthCredentials(), UnauthenticatedUser()

        scope["auth"], scope["user"] = auth_result
        await self.app(scope, receive, send)


class ContextExtensionMiddleware(BaseHTTPMiddleware):
    """Inserts additional names into the template.
    """

    async def dispatch(self, request, call_next):
        """Inserts additional names into the template.
        """
        try:
            context_extensions = getattr(request.state, 'context_extensions')
        except AttributeError:
            context_extensions = {}

        context_extensions['gettext'] = gettext
        context_extensions['translate'] = translate
        context_extensions['user'] = request.user
        context_extensions['lang'] = get_lang(request)
        context_extensions['errors'] = []

        request.state.context_extensions = context_extensions
        response = await call_next(request)
        return response
