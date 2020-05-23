import json
import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from ordnung.storage import storage_settings
from ordnung.storage.database import session
from ordnung.storage.models import User


def get_existing_logins() -> List[str]:
    response = session.query(User.login).all()
    return [x for x, in response]


def get_user_by_login(login: str) -> Optional[User]:
    response = session.query(User).filter_by(login=login).first()
    return response


# def register_new_user(form: dict) -> bool:
#     pass
#
#
# def send_verification_email():
#     pass
