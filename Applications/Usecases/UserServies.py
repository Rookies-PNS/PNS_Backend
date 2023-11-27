import __init__
from typing import List, Optional

from Commons import UserId, Uid, Password, PostId
from Domains.Entities import User, SimpleUser, UserVO
from Applications.Usecases.AppUsecaseExtention import (
    check_valid_password,
    convert_to_Password_with_hashing,
    validate_user_input,
)
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
        self.account_len = 50
        self.name_len = 100


    def create(self, id: str, pw: str, name: str) -> Result[SimpleUser]:
        # check user id
        if self.repository.check_exist_userid(id):
            return Fail_CreateUser_IDAlreadyExists()
        
        match id:
            case valide_id if validate_user_input(valide_id, self.account_len):
                user_id = UserId(account=valide_id)
            case Fail(type=type):
                return Fail(type=f"{type}_in_CreateUser_from_account")

        match name:
            case valide_name if validate_user_input(valide_id, self.name_len):
                checked_name = valide_name
            case Fail(type=type):
                return Fail(type=f"{type}_in_CreateUser_from_name")


        # check passward
        if check_valid_password(pw):
            hash_pw = convert_to_Password_with_hashing(pw)
            match hash_pw:
                case _ if isinstance(hash_pw, Password):
                    password = hash_pw
                case _:
                    return Fail(type="Fail_CreateUser_Invalid_Password")
        else:
            return Fail("Fail_CreateUser_Invalid_Password")

        # create User
        user = User(user_id, checked_name, password)
        return self.repository.save(user)


class LoginUser:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def login(self, id: str, pw: str) -> Result[SimpleUser]:
        # check user id
        if not self.repository.check_exist_userid(id):
            return Fail_CheckUser_IDNotFound()

        # get user
        user = self.repository.search_by_userid(UserId(account=id))

        match user:
            case _ if isinstance(user, UserVO):
                # check pw
                pw = convert_to_Password_with_hashing(pw)
                if pw == user.password:
                    return user.get_simple_user()
        return Fail_CheckUser_PasswardNotCorrect()
