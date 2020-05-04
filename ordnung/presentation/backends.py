# -*- coding: utf-8 -*-

"""Tools related to authorization and network.
"""
import base64
import binascii

from starlette.authentication import (
    AuthCredentials, AuthenticationError, AuthenticationBackend
)
from starlette.authentication import BaseUser as AbstractUser


class BaseUser(AbstractUser):
    @property
    def id(self) -> int:
        raise NotImplementedError()  # pragma: no cover

    @property
    def name(self) -> str:
        return 'Anonymous'

    @property
    def namespace(self):
        raise NotImplementedError()  # pragma: no cover


class UnauthenticatedUser(BaseUser):
    """Class for unauthenticated user representation.
    """

    @property
    def id(self) -> int:
        return 1

    @property
    def name(self) -> str:
        return 'Anonymous'

    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def display_name(self) -> str:
        return ""

    @property
    def namespace(self):
        return "RU"


class User(BaseUser):
    """Class for user representation.
    """

    def __init__(self, username: str) -> None:
        self.username = username

    @property
    def id(self) -> int:
        return 1

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @property
    def namespace(self):
        return "RU"


class OrdnungAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        # TODO: You'd want to verify the username and password here.
        return AuthCredentials(["authenticated"]), User(username)
