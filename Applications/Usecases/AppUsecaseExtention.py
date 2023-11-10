import __init__
from dataclasses import dataclass

from Domains.Entities import User
from Applications.Results import Result
from Commons import Password, UserId


def get_new_user(user_id: str, name: str, pw: str) -> Result[User]:
    pass
