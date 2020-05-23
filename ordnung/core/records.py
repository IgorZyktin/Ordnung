# -*- coding: utf-8 -*-

"""Records handling tools.
"""
from collections import defaultdict
from datetime import date, timedelta
from typing import Optional, Tuple

from sqlalchemy import between

import ordnung.settings
from ordnung.core import core_settings
from ordnung.core.localisation import translate
from ordnung.presentation.backends import User
from ordnung.storage.database import create_new_record, get_existing_record, session
from ordnung.storage.models import Record

# from view.rendering import (
#     fill_select_for_statuses, fill_select_for_persistence, fill_select_for_visibility, translate
# )


def get_records(target_date: date, offset: int = ordnung.settings.MONTH_OFFSET) -> dict:
    # FIXME
    start = target_date - timedelta(days=offset)
    stop = target_date + timedelta(days=offset)

    records = defaultdict(list)

    records_at_date = session.query(Record) \
        .filter(between(Record.target_date, start, stop)) \
        .all()

    # records_at_persistence = session.query(Record) \
    #     .filter_by(persistence_id=3) \
    #     .order_by(Record.status_id).all()

    for record in records_at_date:
        records[str(record.target_date)].append(record)

    # current = start
    # while current <= stop:
    #     for record in records_at_persistence:
    #         if record.persistence_id == 3:
    #             records[str(current)].append(record)
    #
    #     current += timedelta(days=1)

    return records


def get_or_create_record(record_id: Optional[int], chosen_date_str: str,
                         user: User) -> Tuple[Record, dict]:
    """Return record instance and html select element, regardless if this record exists or not.
    """
    sub_context = {}

    record = None
    if record_id is not None:
        record = get_existing_record(record_id)

    if record_id is None or record is None:
        record = create_new_record(user.id, chosen_date_str)
        sub_context['header'] = translate(user.namespace, 'generic', '$new_record')
        sub_context['mode'] = 'create'

    else:
        sub_context['header'] = record.title
        sub_context['mode'] = 'update'

    # sub_context['visibility'] = fill_select_for_visibility(user.namespace, record)
    # sub_context['statuses'] = fill_select_for_statuses(user.namespace, record)
    # sub_context['persistence_types'] = fill_select_for_persistence(user.namespace, record)

    return record, sub_context