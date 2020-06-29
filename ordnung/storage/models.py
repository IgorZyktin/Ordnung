# -*- coding: utf-8 -*-

"""Database models.
"""

from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    Boolean, DateTime, Index, Date, Time, Float,
    ARRAY
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class User(Base):
    """User representation.
    """
    __tablename__ = 'users'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True)
    # -------------------------------------------------------------------------
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    registered = Column(DateTime, nullable=False)
    last_seen = Column(DateTime, nullable=False)
    confirmed = Column(Boolean, nullable=False, default=False)

    groups = relationship('GroupMembership',
                          back_populates="user", collection_class=set)

    parameters = relationship('Parameter',
                              back_populates='user', uselist=False)
    Index('users_idx', 'user_id', 'login', 'email')

    def is_authenticated(self) -> bool:
        """Return True if the user is authenticated.
        """
        return self.confirmed

    def set_password(self, password) -> None:
        """Set new password for the user.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if password is correct.
        """
        return check_password_hash(self.password, password)


class Language(Base):
    """Language representation.
    """
    __tablename__ = 'languages'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    # -------------------------------------------------------------------------
    name = Column(String(255), nullable=False)

    Index('languages_idx', 'id', 'name')


class Country(Base):
    """Country representation.
    """
    __tablename__ = 'countries'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    # -------------------------------------------------------------------------
    name = Column(String(255), nullable=False)

    Index('countries_idx', 'id', 'name')


class Parameter(Base):
    """User defined parameters.
    """
    __tablename__ = 'parameters'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    language_id = Column(Integer, ForeignKey('languages.id'))
    country_id = Column(Integer, ForeignKey('countries.id'))
    # -------------------------------------------------------------------------
    menu_is_visible = Column(Boolean, nullable=False)
    groups_visible = Column(ARRAY(Integer), nullable=False)
    spans_visible = Column(ARRAY(Integer), nullable=False)
    theme = Column(String, nullable=False)
    timezone = Column(String, nullable=False)

    user = relationship('User', back_populates='parameters')
    Index('parameters_idx', 'id', 'user_id')


class Group(Base):
    """User group. Defines visibility of records within group.
    """
    __tablename__ = 'groups'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # -------------------------------------------------------------------------
    name = Column(String(255), nullable=False)

    Index('groups_idx', 'id', 'owner_id')


class GroupMembership(Base):
    """Relation of group memberships.

    One user can have many groups, one group can have many users.
    """
    __tablename__ = 'group_membership'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    # -------------------------------------------------------------------------
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    # -------------------------------------------------------------------------

    user = relationship("User", back_populates="groups")
    group = relationship("Group")

    Index('group_membership_idx', 'user_id', 'group_id')


class Goal(Base):
    """A single task/goal/activity/etc. representation.

    Main component of the application.
    """
    __tablename__ = 'goals'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    span_id = Column(Integer, ForeignKey('span.id'))
    # -------------------------------------------------------------------------
    created_at = Column(DateTime, nullable=False)
    last_edit_at = Column(DateTime, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    target_date = Column(Date)
    target_time = Column(Time)
    actual_from = Column(DateTime, nullable=False)
    actual_to = Column(DateTime)

    Index('goals_idx', 'id', 'user_id', 'group_id', 'span_id')


class Metric(Base):
    """Single measurable goal element.
    """
    __tablename__ = 'metrics'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    goal_id = Column(Integer, ForeignKey('goals.id'))
    # -------------------------------------------------------------------------
    name = Column(String(255), nullable=False)
    increment_name = Column(String(255), nullable=False)
    increment_size = Column(Float, nullable=False, default=0.0)
    objective = Column(Float, nullable=False, default=0.0)

    Index('metrics_idx', 'id', 'user_id', 'goal_id')


class Span(Base):
    """Goal robustness representation.

    Decides how long record lives and how we should
    show it to the user - every day, every week, etc.
    """
    __tablename__ = 'spans'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    # -------------------------------------------------------------------------
    name = Column(String, nullable=False, unique=True)

    Index('spans_idx', 'id', 'name')


class Status(Base):
    """State of a condition. Not condition itself.
    """
    __tablename__ = 'statuses'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    # -------------------------------------------------------------------------
    name = Column(String, nullable=False, unique=True)

    Index('statuses_idx', 'id', 'name')


class Achievement(Base):
    """Actual state of a goal.

    Makes it infinite in time and yet concrete at specific date.
    """
    __tablename__ = 'achievements'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    goal_id = Column(Integer, ForeignKey('goals.id'))
    status_id = Column(Integer, ForeignKey('statuses.id'))
    # -------------------------------------------------------------------------
    event_date = Column(Date, nullable=False)
    event_time = Column(DateTime, nullable=False)
    value = Column(Integer, nullable=False, default=0)

    Index('achievements_idx', 'id', 'user_id',
          'goal_id', 'status_id', 'event_date')
