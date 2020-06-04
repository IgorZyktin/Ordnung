# -*- coding: utf-8 -*-

"""Database access tools.
"""
from typing import Optional

from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from ordnung import settings
from ordnung.core.access import get_now
from ordnung.storage.database import session
from ordnung.storage.models import User, Group, GroupMembership, Visibility


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


def register_user(name: str, login: str, email: str, password: str,
                  language: str) -> int:
    """Register new user.
    """
    try:
        new_user = User(
            name=form.username.data,
            login=form.login.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            registered=get_now(),
            last_seen=get_now(),
            confirmed=False
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        new_user_id = new_user.id

    except IntegrityError:
        session.rollback()
        new_user_id = 0

    if new_user_id:
        new_group = Group(
            owner_id=new_user_id,
            name=settings.DEFAULT_GROUP_NAME,
        )
        session.add(new_group)
        session.commit()
        session.refresh(new_group)

        new_membership = GroupMembership(
            user_id=new_user_id,
            group_id=new_group.id,
        )
        session.add(new_membership)
        session.commit()

        new_visibility = Visibility(
            user_id=new_user_id,
            group_id=new_group.id
        )
        session.add(new_visibility)
        session.commit()

    return new_user_id
