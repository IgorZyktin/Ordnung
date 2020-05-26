# -*- coding: utf-8 -*-

"""Records handling tools.
"""
from collections import defaultdict
from datetime import date, timedelta
from typing import Optional, Tuple, List, Dict

from sqlalchemy import between
from sqlalchemy.engine import ResultProxy

import ordnung.settings
from ordnung import settings
from ordnung.core.localisation import translate
from ordnung.presentation.backends import User
from ordnung.storage.database import session
from ordnung.storage.models import Record

# from view.rendering import (
#     fill_select_for_statuses, fill_select_for_persistence, fill_select_for_visibility, translate
# )


def organize_records(all_records: ResultProxy, current_date: date,
                     offset: int) -> Dict[str, List[dict]]:
    """Split all records into dictionary, with date as key and list of Record as value.
    """
    start = current_date - timedelta(days=offset)
    stop = current_date + timedelta(days=offset)

    records = {}
    current = start
    while current <= stop:
        records[str(current)] = []
        current += timedelta(days=1)

    for record in all_records:
        record_as_dict = {column: value for column, value in record.items()}
        records[str(record.target_date)].append(record_as_dict)

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