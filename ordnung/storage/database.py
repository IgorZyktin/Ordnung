# -*- coding: utf-8 -*-

"""Database tools.
"""
from datetime import date
from typing import Dict, List

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker

from ordnung import settings
from ordnung.core.records import organize_records, sort_nested_records
from ordnung.storage.sql import MEGA_REQUEST

# TODO - check isolation
engine = create_engine(settings.DB_URI, echo=False,
                       isolation_level='AUTOCOMMIT')
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    """Prepare db for work.
    """
    metadata.create_all(bind=engine)


def get_records(target_date: date,
                offset_left: int,
                offset_right: int) -> Dict[str, List[dict]]:
    """Get organized records from database.
    """
    all_records = load_records(target_date, offset_left, offset_right)
    records = organize_records(all_records, target_date,
                               offset_left, offset_right)
    records = sort_nested_records(records)
    return records


def load_records(target_date: date, offset_left: int, offset_right: int,
                 table_name: str = 'test_records'):  # FIXME
    """Retrieve all interesting records from database.

    This function works with extremely complicated SQL request.
    Main goal of doing it like this is to fetch all required resources
    in single action, rather than making a lot of consecutive request.
    In previous version, each Day could retrieve all of it's records
    (in a single request for each persistence type).
    Therefore, we had to do at least 8 x 35 = 280 requests.
    """
    stmt = text(MEGA_REQUEST.format(table_name=table_name))
    return session.execute(stmt, params=dict(target_date=target_date,
                                             offset_left=offset_left,
                                             offset_right=offset_right))
