import __init__
from typing import Optional, List

from Commons import UserId, Uid
from Domains.Entities import UserVO, User
from Applications.Repositories.Interfaces import IUserRepository
from Applications.Results import Result, Fail, Fail_CreateUser_IDAlreadyExists


class TestUserRepositoryList(IUserRepository):
    def __init__(self, arr: List[UserVO]):
        self.arr = arr
        self.count = 0

    def check_not_exist_userid(self, userid: str) -> Result[UserId]:
        for user in self.arr:
            if userid == user.user_id:
                return Fail_CreateUser_IDAlreadyExists
        return UserId(id=userid)

    def save(self, user: User) -> Result[UserVO]:
        self.count += 1
        user_vo = UserVO(user.user_id, user.name, user.password, Uid(idx=self.count))
        self.arr.append(user_vo)

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
