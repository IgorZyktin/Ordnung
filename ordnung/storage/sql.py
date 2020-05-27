# -*- coding: utf-8 -*-

"""Beforehand prepared SQL requests.
"""
ONCE = 1
UNTIL_COMPLETE = 2
EVERY_DAY = 3
EVERY_WEEK = 4
EVERY_ODD_WEEK = 5
EVERY_EVEN_WEEK = 6
EVERY_MONTH = 7
EVERY_YEAR = 8


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

PERSISTENCE_1_SECTION = f"""
-- Persistence <happens_once>
select *
from dates d
         inner join {{table_name}} r on d.cur_date = r.target_date
where r.persistence_id = {ONCE}
"""

PERSISTENCE_2_SECTION = f"""
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

PERSISTENCE_3_SECTION = f"""
-- Persistence <every_day>
select 
    cur_date, 
    first_day, 
    last_day, 
    id, 
    text, 
    persistence_id, 
    start_date, 
    end_date, 
    cur_date as target_date 
from (
select *
from dates d
         cross join {{table_name}} r
where r.persistence_id = {EVERY_DAY}
  and d.cur_date between r.start_date and coalesce(r.end_date, d.last_day)
) as t3
"""

PERSISTENCE_4_SECTION = f"""
-- Persistence <every_week>
select 
    cur_date, 
    first_day, 
    last_day, 
    id, 
    text, 
    persistence_id, 
    start_date, 
    end_date, 
    cur_date as target_date 
from (
select *
from dates d
         cross join {{table_name}} r
where extract(dow from d.cur_date) = extract(dow from r.target_date)
  and r.persistence_id = {EVERY_WEEK}
) as t4
"""

PERSISTENCE_5_SECTION = f"""
-- Persistence <every_odd_week>
select 
    cur_date, 
    first_day, 
    last_day, 
    id, 
    text, 
    persistence_id, 
    start_date, 
    end_date, 
    cur_date as target_date 
from (
select *
from dates d
         cross join {{table_name}} r
where extract(dow from d.cur_date) = extract(dow from r.target_date)
  and r.persistence_id = {EVERY_ODD_WEEK}
    and extract(week from d.cur_date)::int % 2 <> 0
) as t5
"""
PERSISTENCE_6_SECTION = f"""
-- Persistence <every_even_week>
select 
    cur_date, 
    first_day, 
    last_day, 
    id, 
    text, 
    persistence_id, 
    start_date, 
    end_date, 
    cur_date as target_date 
from (
select *
from dates d
         cross join {{table_name}} r
where extract(dow from d.cur_date) = extract(dow from r.target_date)
  and r.persistence_id = {EVERY_EVEN_WEEK}
    and extract(week from d.cur_date)::int % 2 = 0
) as t6
"""

PERSISTENCE_7_SECTION = f"""
-- Persistence <every_month>
select 
    cur_date, 
    first_day, 
    last_day, 
    id, 
    text, 
    persistence_id, 
    start_date, 
    end_date, 
    cur_date as target_date 
from (
select *
from dates d
         cross join {{table_name}} r
where extract(day from d.cur_date) = extract(day from r.target_date)
  and r.persistence_id = {EVERY_MONTH}
) as t7
"""
PERSISTENCE_8_SECTION = f"""
-- Persistence <every_year>
select 
    cur_date, 
    first_day, 
    last_day, 
    id, 
    text, 
    persistence_id, 
    start_date, 
    end_date, 
    cur_date as target_date 
from (
    select *
    from dates d
             cross join {{table_name}} r
    where extract(day from d.cur_date) = extract(day from r.target_date)
      and extract(month from d.cur_date) = extract(month from r.target_date)
      and r.persistence_id = {EVERY_YEAR}
) as t8
"""

MEGA_REQUEST = f"""
{INIT_SECTION}
{PERSISTENCE_1_SECTION}
UNION
{PERSISTENCE_2_SECTION}
UNION
{PERSISTENCE_3_SECTION}
UNION
{PERSISTENCE_4_SECTION}
UNION
{PERSISTENCE_5_SECTION}
UNION
{PERSISTENCE_6_SECTION}
UNION
{PERSISTENCE_7_SECTION}
UNION
{PERSISTENCE_8_SECTION}
order by cur_date;
"""
