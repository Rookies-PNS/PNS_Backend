import __init__
from typing import Optional, List

from Commons import UserId, Uid
from Domains.Entities import UserVO, User
from Applications.Repositories.Interfaces import IUserWriteableRepository
from Applications.Results import (
    Result,
    Fail,
    Fail_CheckUser_IDNotFound,
    Fail_CreateUser_IDAlreadyExists,
)


class TestUserRepositoryList(IUserWriteableRepository):
    def __init__(self, arr: List[UserVO]):
        self.arr = arr
        self.count = 0

    def check_exist_userid(self, userid: str) -> bool:
        for user in self.arr:
            if userid == user.user_id.account:
                return True
        return False

    def save_user(self, user: User) -> Result[UserVO]:
        user_id = self.check_exist_userid(user.user_id)
        self.count += 1
        user_vo = UserVO(user.user_id, user.name, user.password, Uid(idx=self.count))
        self.arr.append(user_vo)
        return user_vo

    def search_by_uid(self, uid: Uid) -> Optional[UserVO]:
        for user in self.arr:
            if uid == user.uid:
                return user
        return None

    def search_by_userid(self, userid: UserId) -> Optional[UserVO]:
        for user in self.arr:
            if userid == user.user_id:
                return user
        return None

    def update(self, user: UserVO) -> Result[UserVO]:
        for i, t_user in enumerate(self.arr):
            if user.uid == t_user.uid:
                self.arr[i] = user
                return user
        return Fail_CreateUser_IDAlreadyExists()

    def delete(self, user: UserVO) -> Result[Uid]:
        self.arr.remove(user)
        return user.uid
