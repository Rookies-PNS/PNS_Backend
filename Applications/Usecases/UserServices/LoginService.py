import __init__
from typing import List, Tuple
from datetime import datetime,timedelta
from Commons import UserId, LoginData,Uid,AuthArchives,PostCounter,UpdateableTime
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
from Applications.Repositories.Interfaces import (
    IUserReadableRepository,
    IUserWriteableRepository,
)
from Applications.Results import (
    Result,
    Fail,
    Fail_CheckUser_IDNotFound,
    Fail_CheckUser_PasswardNotCorrect,
)

# from icecream import ic


class LoginService:
    def __init__(
        self,
        read_repository: IUserReadableRepository,
        write_repository: IUserWriteableRepository,
    ):
        self.repo_r = read_repository
        self.repo_w = write_repository

    def get_block_time(self, num_of_incorrect_login: int) -> int:
        """_summary_
        틀린 횟수에 따른 정지시간을 관리한다.
        Args:
            num_of_incorrect (int): _description_

        Returns:
            int: 제한 하는 분 반환 / 제한을 하지 않으면 0반환
        """
        #
        self.block_rule_list: List[Tuple[int, int]] = [
            (3, 5),  # 3회 틀리면, 5분
            (5, 30),  # 5회 틀리면 30분
            (7, 60),  # 7회 틀리면 1시간
            (9, 1440),  # 9회 틀리면 하루
            (11, 4320),  # 11회 틀리면 3일
        ]
        self.max_block: Tuple[int, int, int] = (
            13,
            2,
            10080,
        )  # 13회 이후부터는 2번 틀릴때마다 일주일씩 블락
        for threshold, block_time in self.block_rule_list:
            if num_of_incorrect_login == threshold:
                return block_time

        # 횟수가 최대 횟수를 초과하는 경우 최대 정지 시간 적용
        match num_of_incorrect_login - self.max_block[0]:
            case minus if minus < 0:  # not max
                return 0
            case up_max:
                return ((up_max + 1) % self.max_block[1]) * self.max_block[2]

    def get_login_data(self, accout: str) -> LoginData:
        return self.repo_r.get_login_data(accout)

    def login(self, id: str, pw: str) -> Result[SimpleUser]:
        # chece validate id
        return SimpleUser(
            user_id=UserId(account='a'),
            nickname='test',
            uid=Uid(idx=1),
            auth=AuthArchives(auths=[]),
            post_count=PostCounter(last_update_date=UpdateableTime(datetime.now())),
        )
        if not validate_account(id):
            return Fail(type=f"Fail_in_LoginUser_InvalidateUserInput_from_account")

        # check login block
        match self.get_login_data(id):
            case login_data if isinstance(login_data, LoginData):
                # 지금 정지 상태인지 확인한다.
                fail_num = login_data.get_count_of_login_fail()
                block_time = self.get_block_time(fail_num)

                if not login_data.check_login_able(block_time):
                    return Fail(type="Fail_in_Login_Block_Account")

                # 한번더 틀리면 정지인지 확인한다.
                block_time = self.get_block_time(fail_num + 1)
                lock_flag = False if block_time == 0 else True
            case _:
                return Fail_CheckUser_IDNotFound()
        # get user
        user = self.repo_r.search_by_userid(id)

        # check passward
        if not check_valid_password(pw):
            self.repo_w.update_to_fail_login(user, lock_flag)
            return Fail("Fail_LoginUser_Invalide_input_pw")
        # get user
        match user:
            case SimpleUser(user_account=account, nickname=nickname):
                hash_pw = convert_to_Password_with_hashing(pw, get_padding_adder(id))
                # success
                if self.repo_r.compare_pw(id, hash_pw):
                    self.repo_w.update_to_success_login(user)
                    return user
            case none if none is None:
                return Fail_CheckUser_IDNotFound()
            case _:
                pass
        # fail
        # ic()
        # ic(lock_flag, fail_num, block_time)
        self.repo_w.update_to_fail_login(user, lock_flag)
        return Fail_CheckUser_PasswardNotCorrect()
