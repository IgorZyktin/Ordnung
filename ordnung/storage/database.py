# -*- coding: utf-8 -*-

"""Database tools.
"""
import time
from datetime import date, timedelta
from typing import Dict, List

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.orm import sessionmaker

from ordnung import settings
from ordnung.storage.sql import MEGA_REQUEST

engine = create_engine(settings.DB_URI, echo=False)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    """Prepare db for work.
    """
    metadata.create_all(bind=engine)


def get_records(target_date: date, offset_left: int, offset_right: int) -> Dict[str, List[dict]]:
    """Get organized records from database.
    """
    all_records = load_records(target_date, offset_left, offset_right)
    records = organize_records(all_records, target_date, offset_left, offset_right)
    return records


def load_records(target_date: date, offset_left: int, offset_right: int,
                 table_name: str = 'test_records') -> ResultProxy:  # FIXME
    """Retrieve all interesting records from database.

    This function works with extremely complicated SQL request.
    Main goal of doing it like this is to fetch all required resources in single action,
    rather than making a lot of consecutive request. In previous version, each Day
    could retrieve all of it's records (in a single request for each persistence type).
    Therefore, we had to do at least 8 x 35 = 280 requests.
    """
    stmt = text(MEGA_REQUEST.format(table_name=table_name))
    records = session.execute(stmt, params=dict(target_date=target_date,
                                                offset_left=offset_left,
                                                offset_right=offset_right))
    return records


def organize_records(all_records: ResultProxy, target_date: date,
                     offset_left: int, offset_right: int) -> Dict[str, List[dict]]:
    """Split all records into dictionary, with date as a key and list of records as value.
    """
    start = target_date - timedelta(days=offset_left)
    stop = target_date + timedelta(days=offset_right)

    records = {}
    current = start
    while current <= stop:
        # We can use defaultdict here, but actual goal is to
        # ensure that all dates are presented in dictionary
        records[str(current)] = []
        current += timedelta(days=1)

    duplicates = set()
    for record in all_records:
        record_as_dict = {column: value for column, value in record.items()}

        id_ = record_as_dict['id']
        key = (id_, record.target_date)

        if str(record.target_date) not in records:
            print('отсутствует дата:', record_as_dict)
        else:

            if key not in duplicates:
                records[str(record.target_date)].append(record_as_dict)
                duplicates.add(key)

    return records


# def create_new_record(user_id: int, chosen_date_str: str) -> Record:
#     """Create new record for given user_id and date.
#     """
#     record = Record(
#         user_id=user_id,
#         target_date=chosen_date_str,
#         title=''
#     )
#     return record
#
#
# def get_existing_record(record_id: int) -> Optional[Record]:
#     """Load from db existing record with this id.
#     """
#     record = session.query(Record).filter_by(id=record_id).first()
#     return record
