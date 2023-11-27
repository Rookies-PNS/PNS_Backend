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
    def get_account(self)->str:
        return self.user_id.account
    def check_equal(self, uid:Optional[Uid])->bool:
        if self.uid ==None:
            return False
        match uid:
            case id if isinstance(id, Uid):
                return uid == self.uid
            case _ :
                return False


@dataclass(frozen=True)
class UserVO:
    user_id: UserId
    name: str
    password: Password
    uid: Uid

    def get_simple_user(self):
        return SimpleUser(user_id=self.user_id, name=self.name, uid=self.uid)

    def get_account(self)->str:
        return self.user_id.account
    def check_equal(self, uid:Optional[Uid])->bool:
        match uid:
            case id if isinstance(id, Uid):
                return uid == self.uid
            case _ :
                return False

@dataclass(frozen=True)
class SimpleUser:
    user_id: UserId
    name: str
    uid: Uid

    def get_account(self)->str:
        return self.user_id.account
    def check_equal(self, uid:Optional[Uid])->bool:
        match uid:
            case id if isinstance(id, Uid):
                return uid == self.uid
            case _ :
                return False