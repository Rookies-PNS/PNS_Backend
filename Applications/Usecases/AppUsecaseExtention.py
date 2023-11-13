import __init__
from dataclasses import dataclass
from typing import Optional

from Domains.Entities import User
from Commons import Password, UserId


def get_new_user(user_id: str, name: str, pw: str) -> Optional[User]:
    pass


def check_valid_password(input_pw: str) -> bool:
    import re

    pattern = re.compile(
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )

    if pattern.match(input_pw):
        return True
    else:
        return False


def convert_to_Password_with_hashing(password: str) -> Optional[Password]:
    import hashlib

    hash = hashlib.sha256()
    hash.update(password.encode("utf-8"))
    hashed_password = hash.hexdigest()
    return Password(pw=hashed_password)
