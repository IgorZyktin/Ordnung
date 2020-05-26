# -*- coding: utf-8 -*-

"""Database tools.
"""
from collections import defaultdict
from datetime import date, timedelta
from typing import Dict, List

from sqlalchemy import create_engine, MetaData, between, text
from sqlalchemy.orm import sessionmaker

from ordnung import settings
from ordnung.storage.models import Record
from ordnung.storage.sql import MEGA_REQUEST

engine = create_engine(settings.DB_URI, echo=True)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    """Prepare db for work.
    """
    metadata.create_all(bind=engine)


def get_records(target_date: date, offset: int, table_name: str = 'records') -> List[Record]:
    """Retrieve all interesting records from database.

    This function works with extremely complicated SQL request.
    Main goal of doing it like this is to fetch all required resources in single action,
    rather than making a lot of consecutive request. In previous version, each Day
    could retrieve all of it's records. Therefore, we had to do at least ~35 requests.
    """
    stmt = text(MEGA_REQUEST.format(table_name=table_name))
    records = session.execute(stmt, params=dict(target_date=target_date, offset=offset))
    return records


def get_records_for_month(target_date: date, user_id: int,
                          user_group: int) -> Dict[str, List[Record]]:
    start = target_date - timedelta(days=settings.MONTH_OFFSET)
    stop = target_date + timedelta(days=settings.MONTH_OFFSET)

    records = defaultdict(list)
    current = start
    while current <= stop:
        records[str(current)] = []
        #     for record in records_at_persistence:
        #         if record.persistence_id == 3:
        #             records[str(current)].append(record)
        #
        current += timedelta(days=1)

    records_at_date = session.query(Record) \
        .filter(between(Record.target_date, start, stop)) \
        .order_by(Record.created_at).all()

    # records_at_persistence = session.query(Record) \
    #     .filter_by(persistence_id=3) \
    #     .order_by(Record.status_id).all()

    for record in records_at_date:
        records[str(record.target_date)].append(record)

    return records

def get_records_in_offset(target_date: date, user_id: int,
                          user_group: int) -> Dict[str, List[Record]]:
    pass


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
