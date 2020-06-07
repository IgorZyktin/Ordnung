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

    groups = relationship("GroupMembership",
                          back_populates="user", collection_class=set)

    parameters = relationship("Parameter",
                              back_populates="user", uselist=False)
    Index('users_id_uindex', 'user_id')

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

    @property
    def lang(self) -> str:
        """Get chosen language for this user.
        """
        # FIXME
        return 'RU'

    @property
    def menu(self) -> bool:
        """Get chosen menu visibility for this user.
        """
        # FIXME
        return False


class Parameter(Base):
    """User defined settings.
    """
    __tablename__ = 'parameters'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    # -------------------------------------------------------------------------
    lang = Column(String, nullable=False)
    menu = Column(Boolean, nullable=False)
    hidden_groups = Column(ARRAY(Integer), nullable=False)
    hidden_persistence = Column(ARRAY(Integer), nullable=False)

    user = relationship("User", back_populates="parameters")


class Group(Base):
    """User group. Defines visibility of records within group.
    """
    __tablename__ = 'groups'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    # -------------------------------------------------------------------------
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    Index('group_idx', 'owner_id')


class GroupMembership(Base):
    """Relation of group memberships.

    One user can have many groups, one group can have many users.
    """
    __tablename__ = 'group_membership'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    # -------------------------------------------------------------------------
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    # -------------------------------------------------------------------------
    Index('group_membership_idx', 'user_id', 'group_id')
    user = relationship("User", back_populates="groups")


class Goal(Base):
    """A single task/goal/activity/etc. representation.

    Main component of the application.
    """
    __tablename__ = 'goals'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    persistence_id = Column(Integer, ForeignKey('persistence.id'))
    # -------------------------------------------------------------------------
    created = Column(DateTime, nullable=False)
    last_edit = Column(DateTime, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    target_date = Column(Date)
    target_time = Column(Time)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    metric_name = Column(String(255), nullable=False)
    metric_objective = Column(Float(), nullable=False)
    metric_step = Column(Float(), nullable=False, default=1)


class Persistence(Base):
    """Persistence representation.

    Decides how long record lives and how we should
    show it to the user - every day, every week, etc.
    """
    __tablename__ = 'persistence'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    # -------------------------------------------------------------------------
    name = Column(String, nullable=False)


class Status(Base):
    """State of a condition. Not condition itself.
    """
    __tablename__ = 'statuses'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    # -------------------------------------------------------------------------
    name = Column(String, nullable=False)


class Achievement(Base):
    """Actual state of a goal.

    Makes it infinite in time and yet concrete at specific date.
    """
    __tablename__ = 'achievements'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    goal_id = Column(Integer, ForeignKey('goals.id'))
    status_id = Column(Integer, ForeignKey('statuses.id'))
    # -------------------------------------------------------------------------
    event_date = Column(Date, nullable=False)
    event_time = Column(DateTime, nullable=False)
    value = Column(Integer, nullable=False, default=0)
