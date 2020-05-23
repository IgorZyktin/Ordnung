# -*- coding: utf-8 -*-

"""Tools related to authorization and network.
"""
import base64
import binascii

from starlette.authentication import (
    AuthCredentials, AuthenticationError, AuthenticationBackend
)
from starlette.authentication import BaseUser as AbstractUser
from starlette.requests import Request
from werkzeug.security import generate_password_hash, check_password_hash

from ordnung.storage.access import get_user_by_login


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

    @property
    def password(self):
        raise NotImplementedError()  # pragma: no cover

    @password.setter
    def password(self, value):
        raise RuntimeError()  # pragma: no cover


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
    def lang(self):
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
    def lang(self):
        return "RU"


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

            if user and check_password_hash(user.password, password):
                return AuthCredentials(["authenticated"]), User(username)
