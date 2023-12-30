import __init__

from Commons import UserId
from Domains.Entities import SimpleUser, UserVO
from Applications.Usecases.AppUsecaseExtention import validate_user_input
from Applications.Usecases.UserServices.UsecaseUserExtention import (
    check_valid_password,
    convert_to_Password_with_hashing,
    get_padding_adder,
    account_len,
    name_len,
    nickname_len,
)
from Applications.Repositories.Interfaces import IUserReadableRepository
from Applications.Results import (
    Result,
    Fail,
    Fail_CheckUser_IDNotFound,
    Fail_CheckUser_PasswardNotCorrect,
)


class LoginService:
    def __init__(self, repository: IUserReadableRepository):
        self.repository = repository

    def login(self, id: str, pw: str) -> Result[SimpleUser]:
        match validate_user_input(id, account_len):
            # invalide user input
            case Fail(type=type):
                return Fail(type=f"{type}_in_LoginUser_invalide_input_id")
            case account if isinstance(account, str):
                checked_id = account
            case _:
                return Fail(type="Fail_LoginUser_Logic_error")

        # check passward
        if not check_valid_password(pw):
            return Fail("Fail_LoginUser_Invalide_input_pw")

        user = self.repository.search_by_userid(UserId(account=checked_id))
        # get user
        match user:
            case SimpleUser(user_id=UserId(account=account), nickname=nickname):
                if self.repository.compare_pw(
                    checked_id,
                    convert_to_Password_with_hashing(
                        pw, get_padding_adder(account, nickname)
                    ),
                ):
                    return user
            case none if none is None:
                return Fail_CheckUser_IDNotFound()
            case _:
                pass
        return Fail_CheckUser_PasswardNotCorrect()
