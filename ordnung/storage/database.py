# -*- coding: utf-8 -*-

"""Database tools.
"""
from typing import Optional

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from ordnung.storage.models import Record
from ordnung.storage import storage_settings

engine = create_engine(storage_settings.DB_PATH, echo=False)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    """Prepare db for work.
    """
    metadata.create_all(bind=engine)


def create_new_record(user_id: int, chosen_date_str: str) -> Record:
    """Create new record for given user_id and date.
    """
    record = Record(
        user_id=user_id,
        target_date=chosen_date_str,
        title=''
    )
    return record


def get_existing_record(record_id: int) -> Optional[Record]:
    """Load from db existing record with this id.
    """
    record = session.query(Record).filter_by(id=record_id).first()
    return record
