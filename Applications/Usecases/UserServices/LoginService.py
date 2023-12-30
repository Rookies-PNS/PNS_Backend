import __init__

from Commons import UserId
from Domains.Entities import SimpleUser, UserVO
from Applications.Usecases.AppUsecaseExtention import validate_user_input
from Applications.Usecases.UserServices.UsecaseUserExtention import (
    check_valid_password,
    convert_to_Password_with_hashing,
    get_padding_adder,
    validate_account,
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
        # chece validate id
        if not validate_account(id):
            return Fail(type=f"Fail_in_LoginUser_InvalidateUserInput_from_account")

        # check passward
        if not check_valid_password(pw):
            return Fail("Fail_LoginUser_Invalide_input_pw")

        user = self.repository.search_by_userid(UserId(account=id))
        # get user
        match user:
            case SimpleUser(user_id=account, nickname=nickname):
                hash_pw = convert_to_Password_with_hashing(pw, get_padding_adder(id))
                if self.repository.compare_pw(account, hash_pw):
                    return user
            case none if none is None:
                return Fail_CheckUser_IDNotFound()
            case _:
                pass
        return Fail_CheckUser_PasswardNotCorrect()
