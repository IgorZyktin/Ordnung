# -*- coding: utf-8 -*-

"""Database access tools.
"""
from datetime import date
from typing import Optional, List, Tuple

from sqlalchemy import or_, func, text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from ordnung import settings
from ordnung.core.access import get_now
from ordnung.storage.database import session
from ordnung.storage.models import User, Group, GroupMembership, Parameter, \
    Span, Status


def get_holidays(country: str, target_date: date, offset_left: int,
                 offset_right: int) -> List[Tuple[date, str]]:
    """Get list of holidays for specified country.
    WITH dates_list AS (
	SELECT (generate_series(date('2020-06-10') - 20,
							date('2020-06-10') + 20,
							'1 day'::interval)::date) AS event_date
)
SELECT * FROM dates_list dl
LEFT JOIN (
	SELECT * FROM holidays WHERE country_id = (
		SELECT id FROM countries
		WHERE name = 'Russia' LIMIT 1)) h
ON h.event_date = dl.event_date
ORDER BY dl.event_date;
    """
    stmt = text("""
    WITH user_country AS (
        SELECT id 
        FROM countries 
        WHERE name = :user_country 
        LIMIT 1
    ),
        dates_list AS (
        SELECT (generate_series(date(:target_date) - :offset_left,
                                date(:target_date) + :offset_right, 
                                '1 day'::interval)::date) AS event_date
    )
    SELECT * FROM dates_list dl
    LEFT JOIN (SELECT * FROM holidays WHERE country_id = user_country.id) h
    ON h.event_date = dl.event_date
    ORDER BY dl.event_date;
    """)
    return list(session.execute(stmt, params=dict(user_country=country,
                                             target_date=target_date,
                                             offset_left=offset_left,
                                             offset_right=offset_right)))


def get_user_by_id(user_id: int) -> Optional[User]:
    """Go to DB and search user by the specified user id.
    """
    return session.query(User).filter_by(id=user_id).first()


def get_user_by_login(login: str) -> Optional[User]:
    """Go to DB and search user by the specified login. Case insensitive.
    """
    response = session.query(User).filter(
        func.lower(User.login) == login.lower()
    ).first()
    return response


def get_user_by_email_or_login(user_contact: str) -> Optional[User]:
    """Go to DB and search user by the specified login/email. Case insensitive.
    """
    response = session.query(User).filter(
        or_(
            func.lower(User.login) == user_contact.lower(),
            func.lower(User.email) == user_contact.lower(),
        )
    ).first()
    return response


def get_span_types() -> List[Span]:
    """Get all available persistence types.
    """
    return session.query(Span).order_by('id').all()


def get_status_types() -> List[Status]:
    """Get all available status types.
    """
    return session.query(Status).order_by('id').all()


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


def register_user(name: str, login: str, email: str,
                  password: str, language: str) -> int:
    """Register new user.
    """
    try:
        with session.begin(subtransactions=True):
            new_user = User(
                name=name,
                login=login,
                email=email,
                password=generate_password_hash(password),
                registered=get_now(),
                last_seen=get_now(),
                confirmed=False
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            new_user_id = new_user.id

            with session.begin(subtransactions=True):
                new_group = Group(
                    owner_id=new_user_id,
                    name=settings.DEFAULT_GROUP_NAME,
                )
                session.add(new_group)
                session.commit()
                session.refresh(new_group)

                new_parameter = Parameter(
                    user_id=new_user_id,
                    lang=language,
                    menu=False,
                )
                session.add(new_parameter)
                session.commit()

                with session.begin(subtransactions=True):
                    new_membership = GroupMembership(
                        user_id=new_user_id,
                        group_id=new_group.id,
                    )
                    session.add(new_membership)
                    session.commit()

            session.commit()
    except IntegrityError:
        session.rollback()
        new_user_id = 0

    return new_user_id


def drop_user(user_id: int) -> bool:
    """Remove user and all corresponding records.
    """
    # TODO
    groups = 0
    membership = 0
    parameters = 0
    goals = 0
    achievements = 0

    with session.begin_nested():
        user_groups = session.query(Group).filter_by(owner_id=user_id)
        for group in user_groups:
            session.delete(group)
    return False
