# -*- coding: utf-8 -*-

"""Project parameters.
"""
import sys

from ordnung.presentation.access import get_local_ip

#  ------------------ CORE SETTINGS ------------------

# date and time
STEP_SIZE = 7  # days
LEAP_SIZE = 21  # days
WEEKENDS = {5, 6}  # weekday indexes, saturday and sunday
WEEK_LENGTH = 7
WEEKS_IN_MONTH = 5
MONTH_OFFSET = 20  # additional days to search in both directions during month rendering
MAX_RECORDS_IN_MENU = 20

# localisation
DEFAULT_LANG = 'EN'
DEFAULT_PLACEHOLDER = '???'

#  ----------------- STORAGE SETTINGS ----------------

LOGGER_FILENAME = 'ordnung.log'
LOGGER_ROTATION = '1 week'
DB_PATH = 'sqlite:///database.db'

#  -------------- PRESENTATION SETTINGS --------------

if sys.platform == 'win32':
    # for lan broadcasting
    HOST = get_local_ip()
else:
    HOST = '127.0.0.1'

PORT = 8000
DEBUG = True
RELOAD = True
