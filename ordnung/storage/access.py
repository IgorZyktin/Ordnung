from typing import List, Optional

from ordnung.storage.database import session
from ordnung.storage.models import User


def get_existing_logins() -> List[str]:
    response = session.query(User.login).all()
    return [x for x, in response]


def get_user_by_login(login: str) -> Optional[User]:
    response = session.query(User).filter_by(login=login).first()
    return response
