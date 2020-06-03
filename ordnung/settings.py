# -*- coding: utf-8 -*-

"""Project parameters.
"""
import os
import sys

#  ------------------ CORE SETTINGS ------------------
from typing import Literal

SECRET_KEY = os.getenv('ORDNUNG_SECRET_KEY')

# date and time
STEP_SIZE = 7  # days
LEAP_SIZE = 21  # days
WEEKENDS = {5, 6}  # weekday indexes, saturday and sunday
WEEK_LENGTH = 7
WEEKS_IN_MONTH = 5

# additional days to search in both directions during month rendering
MONTH_OFFSET = 20
MAX_RECORDS_IN_MENU = 20

# localisation
DEFAULT_LANG = 'EN'
DEFAULT_PLACEHOLDER = '???'

MAX_PASSWORD_RESTORE_INTERVAL = 86400
DEFAULT_GROUP_NAME = 'Home'

#  ----------------- STORAGE SETTINGS ----------------

LOGGER_FILENAME = 'ordnung.log'
LOGGER_ROTATION = '1 week'
DB_URI = os.getenv('ORDNUNG_DB_URI')

#  -------------- PRESENTATION SETTINGS --------------

if sys.platform == 'win32':
    DEBUG = True
    RELOAD = True

else:
    DEBUG = False
    RELOAD = False

HOST = '127.0.0.1'
PORT = 8000
URL_STYLE: Literal['absolute', 'relative'] = 'relative'
URL_STYLE: Literal['absolute', 'relative'] = 'absolute'

EMAIL_DEFAULT_ADDRESS = 'ordnung.auto@gmail.com'
EMAIL_LOGIN = 'ordnung.auto'
EMAIL_PASSWORD = os.getenv('ORDNUNG_EMAIL_PASSWORD')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
