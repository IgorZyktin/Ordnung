# -*- coding: utf-8 -*-

"""Database models.
"""

from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    UniqueConstraint, Boolean, DateTime, Index
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User representation.

    Please note, that application itself (login/logout, etc.)
    rely not on this exact model, but on it's specific user
    class! This one is only for database manipulations.
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
    Index('users_id_uindex', 'user_id')


class Group(Base):
    """User group. Defines visibility of records within group.
    """
    __tablename__ = 'groups'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True)
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
    id = Column(Integer, primary_key=True)
    # -------------------------------------------------------------------------
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    # -------------------------------------------------------------------------
    Index('group_membership_idx', 'user_id', 'group_id')


class Visibility(Base):
    """Visible user groups.
    """
    __tablename__ = 'visibility'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True)
    # -------------------------------------------------------------------------
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    UniqueConstraint('user_id', 'group_id')
    Index('visibility_idx', 'user_id', 'group_id')


class Record(Base):
    """A single task/goal/activity/etc. representation.

    Main component of the application.
    """
    __tablename__ = 'records'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    persistence_id = Column(Integer, ForeignKey('persistence.id'))
    # -------------------------------------------------------------------------
    created_at = Column(String, nullable=False)
    last_edit = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    target_date = Column(String, nullable=False)
    target_time = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String)


class Persistence(Base):
    """Persistence representation.

    Decides how long record lives and how we should
    show it to the user - every day, every week, etc.
    """
    __tablename__ = 'persistence'
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True)
    # -------------------------------------------------------------------------
    name = Column(String, nullable=False)


# class Comment(Base):
#     """A single comment representation.
#     """
#     __tablename__ = 'comments'
#     # -------------------------------------------------------------------------
#     id = Column(Integer, primary_key=True)
#     record_id = Column(Integer, ForeignKey('records.id'))
#     user_id = Column(Integer, ForeignKey('users.id'))
#     # -------------------------------------------------------------------------
#     created_at = Column(String, nullable=False)
#     text = Column(String, nullable=False)


# class Status(Base):
#     """Name of a condition. Not condition itself.
#     """
#     __tablename__ = 'statuses'
#     # ----------------------------------------------------------------------------------------------
#     id = Column(Integer, primary_key=True)
#     # ----------------------------------------------------------------------------------------------
#     name = Column(String, nullable=False)
#
#
# class Achievement(Base):
#     """Actual state of a record. Makes it infinite in time and yet concrete at specific date.
#     """
#     __tablename__ = 'achievement'
#     # ----------------------------------------------------------------------------------------------
#     id = Column(Integer, primary_key=True)
#     record_id = Column(Integer, ForeignKey('records.id'))
#     status_id = Column(Integer, ForeignKey('statuses.id'))
#     # ----------------------------------------------------------------------------------------------
#     event_time = Column(String, nullable=False)
#     event_value = Column(Integer, nullable=False, default=0)
