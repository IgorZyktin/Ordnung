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
    async def authenticate(self, request: Request):
        auth_cookie = request.cookies.get('Authorization')

        if not auth_cookie:
            return
        print('пытаемся зайти', request.url, auth_cookie)
        try:
            scheme, credentials = auth_cookie.split()
            if scheme.lower() != 'basic':
                return

            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        user = get_user_by_login(username)
        print('у нас пользователь', user)
        if user and check_password_hash(user.password, password):
            return AuthCredentials(["authenticated"]), User(username)
