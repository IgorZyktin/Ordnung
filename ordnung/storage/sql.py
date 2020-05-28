# -*- coding: utf-8 -*-

"""Beforehand prepared SQL requests.
"""
ONCE = 1
UNTIL_COMPLETE = 2
EVERY_DAY = 3
EVERY_WEEK = 4
EVERY_ODD_WEEK = 5
EVERY_EVEN_WEEK = 6
FIRST_DAY_OF_MONTH = 7
LAST_DAY_OF_MONTH = 8
EVERY_MONTH = 9
EVERY_YEAR = 10

INIT_SECTION = r"""
with date_list as (
    select (generate_series(date(:target_date) - :offset_left,
                            date(:target_date) + :offset_right, 
                            '1 day'::interval)::date) as cur_date
    ),
     dates as (
         select *
         from date_list
                  cross join (select min(cur_date) as first_day from date_list) as first_day
                  cross join (select max(cur_date) as last_day from date_list) as last_day
     )
"""

PERSISTENCE_01_SECTION = f"""
-- Persistence <happens_once>
select *
from dates d
         inner join {{table_name}} r on d.cur_date = r.target_date
where r.persistence_id = {ONCE}
"""

PERSISTENCE_02_SECTION = f"""
-- Persistence <until_complete>
select *
from (
         select *
         from dates
                  cross join {{table_name}} r
         where r.persistence_id = {UNTIL_COMPLETE}
     ) as r
where r.cur_date between r.start_date and coalesce(r.end_date, r.target_date)
"""

PERSISTENCE_03_SECTION = f"""
-- Persistence <every_day>
select *
from dates d
         cross join {{table_name}} r
where r.persistence_id = {EVERY_DAY}
  and d.cur_date between r.start_date and coalesce(r.end_date, d.last_day)
"""

PERSISTENCE_04_SECTION = f"""
-- Persistence <every_week>
select *
from dates d
         cross join {{table_name}} r
where extract(dow from d.cur_date) = extract(dow from r.target_date)
  and r.persistence_id = {EVERY_WEEK}
"""

PERSISTENCE_05_SECTION = f"""
-- Persistence <every_odd_week>
select *
from dates d
         cross join {{table_name}} r
where extract(dow from d.cur_date) = extract(dow from r.target_date)
  and r.persistence_id = {EVERY_ODD_WEEK}
    and extract(week from d.cur_date)::int % 2 <> 0
"""
PERSISTENCE_06_SECTION = f"""
-- Persistence <every_even_week>
select *
from dates d
         cross join {{table_name}} r
where extract(dow from d.cur_date) = extract(dow from r.target_date)
  and r.persistence_id = {EVERY_EVEN_WEEK}
    and extract(week from d.cur_date)::int % 2 = 0
"""

PERSISTENCE_07_SECTION = f"""
-- Persistence <first_day_of_month>
select * 
from dates d 
        cross join {{table_name}} r
where extract(day from d.cur_date) = 1 and r.persistence_id = {FIRST_DAY_OF_MONTH}
"""

PERSISTENCE_08_SECTION = f"""
-- Persistence <last_day_of_month>
select * 
from dates d 
        cross join {{table_name}} r
where extract(day from d.cur_date) 
        = extract(days FROM date_trunc('month', cur_date) + interval '1 month - 1 day')
  and r.persistence_id = {LAST_DAY_OF_MONTH}
"""

PERSISTENCE_09_SECTION = f"""
-- Persistence <every_month>
select * 
from dates d 
        cross join {{table_name}} r
where extract(day from d.cur_date) = extract(day from r.target_date) 
  and r.persistence_id = {EVERY_MONTH}
"""

PERSISTENCE_10_SECTION = f"""
-- Persistence <every_year>
select *
from dates d
         cross join {{table_name}} r
where extract(day from d.cur_date) = extract(day from r.target_date)
  and extract(month from d.cur_date) = extract(month from r.target_date)
  and r.persistence_id = {EVERY_YEAR}
"""

MEGA_REQUEST = f"""
{INIT_SECTION}
{PERSISTENCE_01_SECTION}
UNION
{PERSISTENCE_02_SECTION}
UNION
{PERSISTENCE_03_SECTION}
UNION
{PERSISTENCE_04_SECTION}
UNION
{PERSISTENCE_05_SECTION}
UNION
{PERSISTENCE_06_SECTION}
UNION
{PERSISTENCE_07_SECTION}
UNION
{PERSISTENCE_08_SECTION}
UNION
{PERSISTENCE_09_SECTION}
UNION
{PERSISTENCE_10_SECTION}
order by cur_date;
"""
