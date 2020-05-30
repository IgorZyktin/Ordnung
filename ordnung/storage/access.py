# -*- coding: utf-8 -*-

"""Database access tools.
"""
from typing import Optional

from sqlalchemy import or_, func

from ordnung.storage.database import session
from ordnung.storage.models import User


def get_user_by_id(user_id: int) -> Optional[User]:
    """Go to DB and search for the specified user id.
    """
    return session.query(User).filter_by(id=user_id).first()


def get_user_by_login(login: str) -> Optional[User]:
    """Go to DB and search for the specified login. Case insensitive.
    """
    response = session.query(User).filter(
        func.lower(User.login) == login.lower()
    ).first()

    return response


def get_user_by_email_or_login(user_contact: str) -> Optional[User]:
    """Go to DB and search for the specified login/email. Case insensitive.
    """
    response = session.query(User).filter(
        or_(
            func.lower(User.login) == user_contact.lower(),
            func.lower(User.email) == user_contact.lower(),
        )
    ).first()

    return response
