from typing import List, Optional
from dataclasses import dataclass

from Commons import UserId, Uid, Password, PostId


class User:
    def __init__(
        self,
        user_id: UserId,
        name: str,
        password: Password,
        uid: Optional[Uid] = None,
    ):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.uid = uid


@dataclass(frozen=True)
class UserVO:
    user_id: UserId
    name: str
    password: Password
    uid: Uid

    def get_simple_user(self):
        return SimpleUser(user_id=self.user_id, name=self.name, uid=self.uid)


@dataclass(frozen=True)
class SimpleUser:
    user_id: UserId
    name: str
    uid: Uid
