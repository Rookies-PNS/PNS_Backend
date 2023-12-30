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
    TargetScope,
    Auth,
    AuthArchives,
)
from Domains.Entities import User
from Applications.Usecases.AppUsecaseExtention import validate_user_input

from Applications.Usecases.UserServices.UsecaseUserExtention import (
    check_valid_password,
    convert_to_Password_with_hashing,
    get_padding_adder,
    validate_account,
    validate_name,
    validate_nickname,
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
        self.basic_login_data = LoginData(
            time_of_try_login=UpdateableTime(datetime.now())
        )
        self.basic_post_counter = PostCounter(UpdateableTime(datetime.now()))

    def create(
        self,
        account: str,
        passwd: str,
        name: str,
        nickname: str,
        auths: List[Auth] = [  # Nomal User Auth List
            Auth(Policy.UserDataReadAblePolicy, TargetScope.Own),  # 자신의 유저 정보 열람가능
            Auth(Policy.UserDataDeleteAblePolicy, TargetScope.Own),  # 자기 계정 삭제가능
            Auth(Policy.PostReadAblePolicy, TargetScope.Allowed),  # 공개된 일기 읽기 가능
            Auth(Policy.PostReadAblePolicy, TargetScope.Own),  # 자기 일기 읽기 가능
            Auth(Policy.PostDeleteAblePolicy, TargetScope.Own),  # 자기 일기 삭제가능
            Auth(Policy.PostCreateAndUpdateAblePolicy, TargetScope.Own),  # 자기 일기 수정가능
            Auth(Policy.PostPublicAblePolicy, TargetScope.Own),  # 자기 일기 공개가능
            Auth(Policy.PostPrivateAblePolicy, TargetScope.Own),  # 자기 일기 비공개가능
        ],
    ) -> Optional[Fail]:
        # chece validate id
        if not validate_account(account):
            return Fail(type=f"Fail_in_CreateUser_InvalidateUserInput_from_account")

        if self.repository.check_exist_userid(account):
            return Fail_CreateUser_IDAlreadyExists()
        user_account = UserId(account=account)

        # check validate name
        if validate_name(name):
            checked_name = name
        else:
            return Fail(type=f"Fail_in_CreateUser_InvalidateUserInput_from_name")

        # check validate nickname
        if validate_nickname(nickname):
            checked_nickname = nickname
        else:
            return Fail(type=f"Fail_in_CreateUser_InvalidateUserInput_from_nickname")

        # check passward
        if not check_valid_password(passwd):
            return Fail("Fail_CreateUser_Invalid_Password")

        match convert_to_Password_with_hashing(passwd, get_padding_adder(account)):
            case hash_pw if isinstance(hash_pw, Password):
                password = hash_pw
            case _:
                return Fail(type="Fail_CreateUser_Invalid_Password")

        match auths:
            case []:
                return Fail(type="Fail_CreateUser_NoAuth")
            case auth if isinstance(auth, list):
                archives = AuthArchives(auths=auths)
            case _:
                return Fail(type="Fail_CreateUser_Typeerror_in_auth")

        # create User
        user = User(
            pw=password,
            user_account=user_account,
            name=checked_name,
            nickname=checked_nickname,
            auth=archives,
            login_data=self.basic_login_data,
            post_count=self.basic_post_counter,
        )
        return self.repository.save_user(user)
