import __init__
from typing import List, Optional

from Commons import UserId, Uid, Password, PostId
from Domains.Entities import User, UserVO
from Applications.Repositories.Interfaces import IUserRepository
from Applications.Results import (
    Result,
    Fail,
    Fail_CreateUser_IDAlreadyExists,
    Fail_CheckUser_IDNotFound,
    Fail_CheckUser_PasswardNotCorrect,
)


class CreateUser:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def create(self, id: str, pw: str, name: str) -> Result[UserVO]:
        # check user id
        if self.repository.check_exist_userid(id):
            return Fail_CreateUser_IDAlreadyExists()
        user_id = UserId(id=id)

        # check passward
        password = Password(pw=pw)

        # create User
        user = User(user_id, name, password)
        return self.repository.save(user)


class LoginUser:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def login(self, id: str, pw: str) -> Result[UserVO]:
        # check user id
        if not self.repository.check_exist_userid(id):
            return Fail_CheckUser_IDNotFound()

        # get user
        user = self.repository.search_by_userid(UserId(id=id))

        # check pw
        pw = Password(pw=pw)
        if pw == user.password:
            return user
        return Fail_CheckUser_PasswardNotCorrect()
