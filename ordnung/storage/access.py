# -*- coding: utf-8 -*-

"""Database access tools.
"""
from typing import Optional

from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from ordnung.core.access import get_now
from ordnung.presentation.forms import RegisterForm
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


def change_user_password(user_id: int, new_password: str) -> bool:
    """Change user password, return True on success.
    """
    user = get_user_by_id(user_id)

    if user is not None:
        user.password = generate_password_hash(new_password)
        session.add(user)
        session.commit()
        return True
    return False


def confirm_registration(user_id: int) -> bool:
    """Confirm user as valid, return True on success.
    """
    user = get_user_by_id(user_id)

    if user is not None:
        user.confirmed = True
        session.add(user)
        session.commit()
        return True
    return False


def register_new_user(form: RegisterForm) -> int:
    """Register new user.
    """
    new_user = User(
        name=form.username.data,
        email=form.email.data,
        login=form.login.data,
        password=generate_password_hash(form.password.data),
        registered=get_now(),
        last_seen=get_now(),
        confirmed=False
    )
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        new_id = new_user.id
    except IntegrityError:
        new_id = 0
    return new_id
