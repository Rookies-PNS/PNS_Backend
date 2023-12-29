import __init__
from typing import Optional, List
from datetime import datetime

from Commons import (
    UserId,
    Password,
    UpdateableTime,
    LoginData,
    PostCounter,
    Policy,
    TargetRange,
    Auth,
    AuthArchives,
)
from Domains.Entities import User
from Applications.Usecases.AppUsecaseExtention import validate_user_input

from Applications.Usecases.UserServices.UsecaseUserExtention import (
    check_valid_password,
    convert_to_Password_with_hashing,
    get_padding_adder,
    account_len,
    name_len,
    nickname_len,
)
from Applications.Repositories.Interfaces import IUserWriteableRepository
from Applications.Results import (
    Result,
    Fail,
    Fail_CreateUser_IDAlreadyExists,
)


class CreateUserService:
    def __init__(self, repository: IUserWriteableRepository):
        self.repository = repository
        self.account_len = account_len
        self.name_len = name_len
        self.nickname_len = nickname_len
        self.basic_login_data = LoginData(lock_time=UpdateableTime(datetime.now()))
        self.basic_post_counter = PostCounter(UpdateableTime(datetime.now()))

    def create(
        self,
        account: str,
        passwd: str,
        name: str,
        nickname: str,
        auths: List[Auth] = [  # Nomal User Auth List
            Auth(Policy.UserDataReadAblePolicy, TargetRange.Allowed),
            Auth(Policy.UserDataReadAblePolicy, TargetRange.Own),
            Auth(Policy.PostCreateAndUpdateAblePolicy, TargetRange.Own),
            Auth(Policy.PostDeleteAblePolicy, TargetRange.Own),
            Auth(Policy.PostPublicAblePolicy, TargetRange.Own),
            Auth(Policy.PostPrivateAblePolicy, TargetRange.Own),
            Auth(Policy.UserDataReadAblePolicy, TargetRange.Own),
            Auth(Policy.UserDataDeleteAblePolicy, TargetRange.Own),
        ],
    ) -> Optional[Fail]:
        # chece validate id
        match validate_user_input(account, self.account_len):
            # invalide user input
            case Fail(type=type):
                return Fail(type=f"{type}_in_CreateUser_from_account")
            # check user id
            case str(valide_account) if not self.repository.check_exist_userid(
                valide_account
            ):
                if self.repository.check_exist_userid(valide_account):
                    return Fail_CreateUser_IDAlreadyExists()
                user_account = UserId(account=valide_account)
            case _:
                return Fail(type=f"Fail_type_error_CreateUser_from_account")

        # check validate name
        match validate_user_input(name, self.name_len):
            case Fail(type=type):
                return Fail(type=f"{type}_in_CreateUser_from_name")
            case valide_name if isinstance(valide_name, str):
                checked_name = valide_name
            case _:
                return Fail(type="Fail_type_error_CreateUser_from_name")
        # check validate nickname
        match validate_user_input(nickname, self.nickname_len):
            case Fail(type=type):
                return Fail(type=f"{type}_in_CreateUser_from_nickname")
            case valide_name if isinstance(valide_name, str):
                checked_nickname = valide_name
            case _:
                return Fail(type="Fail_type_error_CreateUser_from_nickname")
        # check passward
        if not check_valid_password(passwd):
            return Fail("Fail_CreateUser_Invalid_Password")

        match convert_to_Password_with_hashing(
            passwd, get_padding_adder(account, nickname)
        ):
            case hash_pw if isinstance(hash_pw, Password):
                password = hash_pw
            case _:
                return Fail(type="Fail_CreateUser_Invalid_Password")

        match auths:
            case []:
                return Fail(type="Fail_CreateUser_NoAuth")
            case auth if isinstance(auth, List[Auth]):
                archives = AuthArchives(auths=auths)
            case _:
                return Fail(type="Fail_CreateUser_Typeerror_in_auth")

        # create User
        user = User(
            pw=password,
            user_id=user_account,
            name=checked_name,
            nickname=checked_nickname,
            auth=archives,
            login_data=self.basic_login_data,
            post_count=self.basic_post_counter,
        )
        return self.repository.save_user(user)
