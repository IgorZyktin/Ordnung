# -*- coding: utf-8 -*-

"""Records handling tools.
"""
from datetime import date, timedelta
from typing import List, Dict, Callable

Records = Dict[str, List[dict]]


def sort_by_persistence(raw_record: dict) -> int:
    """Key function, created to sort by persistence_id.
    """
    return raw_record.get('persistence_id', 999)


def organize_records(all_records, target_date: date, offset_left: int,
                     offset_right: int) -> Records:
    """Split all records into dictionary.

    Date as a key and list of records as value.

    Example output:
    {
        '2020-05-08':
        [
            {
                'id': 9,
                'cur_date': datetime.date(2020, 5, 8),
                'first_day': datetime.date(2020, 5, 8),
                'last_day': datetime.date(2020, 6, 17),
                'text': 'text',
                'persistence_id': 3,
                'start_date': datetime.date(2020, 5, 1),
                'end_date': None,
                'target_date': datetime.date(2020, 5, 19),
                ...
            }
        ]
    }
    """
    start = target_date - timedelta(days=offset_left)
    stop = target_date + timedelta(days=offset_right)

    records = {}
    cur_date = start
    while cur_date <= stop:
        # We can use defaultdict here, but actual goal is to
        # ensure that all dates are presented in the dictionary
        records[str(cur_date)] = []
        cur_date += timedelta(days=1)

    duplicates = set()
    for record in all_records:
        record_as_dict = {column: value for column, value in record.items()}

        id_ = record_as_dict['id']
        key = (id_, record.cur_date)

        if str(record.cur_date) not in records:
            raise ValueError(f'Date {record.cur_date} is not '
                             f'found in record {record_as_dict}')

        if key not in duplicates:
            records[str(record.cur_date)].append(record_as_dict)
            duplicates.add(key)

    return records


def sort_nested_records(records: Records,
                        sorter: Callable = sort_by_persistence) -> Records:
    """Sort dictionary with records by given sorter.
    """
    sorted_records = {}

    for day_date, day_records in records.items():
        sorted_records[day_date] = sorted(day_records, key=sorter)

    return sorted_records
