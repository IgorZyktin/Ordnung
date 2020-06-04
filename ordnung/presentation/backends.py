# -*- coding: utf-8 -*-

"""Tools related to authorization and network.
"""
import base64
import binascii

from starlette.authentication import (
    AuthCredentials, AuthenticationError, AuthenticationBackend
)
from starlette.requests import Request

from ordnung.storage.access import get_user_by_login


class OrdnungAuthBackend(AuthenticationBackend):
    """Authentication backend, that handles user distinction.
    """

    async def authenticate(self, request: Request):
        """Runs on every request.
        """
        auth = request.headers.get("Authorization", '')

        if auth:
            try:
                scheme, credentials = auth.split()
                if scheme.lower() != 'basic':
                    return None

                decoded = base64.b64decode(credentials).decode("ascii")
            except (ValueError, UnicodeDecodeError, binascii.Error):
                raise AuthenticationError('Invalid basic auth credentials')

            username, _, password = decoded.partition(":")
            user = get_user_by_login(username)

            if user and user.check_password(password):
                return AuthCredentials(["authenticated"]), user
