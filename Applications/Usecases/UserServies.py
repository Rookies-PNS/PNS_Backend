import __init__
from typing import List, Optional

from Commons import UserId, Uid, Password, PostId
from Domains.Models import User, UserVO
from Applications.Repositories.Interfaces import IUserRepository
from Applications.Results import Result, Fail


class CreateUser:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def create(self, id: str, pw: str, name: str) -> Result[UserVO]:
        # check user id
        ret_uid = self.repository.check_not_exist_userid(id)
        match ret_uid:
            case _ if isinstance(ret_uid, UserId):
                user_id: UserId = ret_uid
            case _:
                return ret_uid

        # check passward
        password = Password(pw=pw)

        # create User
        user = User(user_id, name, password)
        return self.repository.save(user)
