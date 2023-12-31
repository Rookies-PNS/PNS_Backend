from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


from Commons import (
    UserId,
    Uid,
    Password,
    AuthArchives,
    LoginData,
    PostCounter,
    Policy,
    TargetScope,
)


class CommonUserAction:
    user_account: UserId
    nickname: str
    uid: Uid
    auth: AuthArchives
    post_count: PostCounter

    def get_account(self) -> str:
        return self.user_account.account

    def check_equal_uid(self, uid: Optional[Uid]) -> bool:
        match uid:
            case id if isinstance(id, Uid):
                return uid == self.uid
            case _:
                return False

    def get_user_nickname(self) -> str:
        return self.nickname

    def get_uid(self) -> Uid:
        return self.uid

    def count_post_num(self):
        """
        현재 날짜와 last_update_date를 비교하여 게시물 수를 업데이트하는 메서드
        """
        return self.post_count.count_post_num()

    def get_post_num(self) -> int:
        """
        게시물 수를 반환하는 메서드
        """
        return self.post_count.get_post_num()

    def check_policy(self, policy: Policy) -> List[TargetScope]:
        """_summary_
        정책(policy)을 소유여 부를 확인하고, 유효범위(TargetRange)를 반환한다.

        Args:
            policy (Policy): 알고자 하는 정책

        Returns:
            List[TargetRange]: 정책이 같은 모든 유효범위 반환(TargetScope), 없으면 empty list 반환
        """
        return self.auth.check_policy(policy)


@dataclass(frozen=True)
class SimpleUser(CommonUserAction):
    """
    가장 기본적인 유저 데이터
    """

    user_account: UserId
    nickname: str
    uid: Uid
    auth: AuthArchives
    post_count: PostCounter


class SecurityUesrAction(CommonUserAction):
    login_data: LoginData

    def get_count_of_login_fail(self) -> int:
        return self.login_data.get_count_of_login_fail()

    def get_due_to_of_login_lock(self) -> datetime:
        return self.login_data.get_due_to_of_login_lock()

    def check_login_able(self, block_minute: int) -> bool:
        """
        로그인 가능 여부를 확인하는 함수
        """
        return self.login_data.check_login_able(block_minute)

    def fail_login(self):
        return self.login_data.fail_login()

    def success_login(self):
        return self.login_data.success_login()

    def lock_login(self):
        return self.login_data.lock_login()


@dataclass(frozen=True)
class SecuritySimpleUser(SecurityUesrAction):
    """
    차후 관리자가 사용하게 될 유저 데이터
    """

    user_account: UserId
    nickname: str
    uid: Uid
    auth: AuthArchives
    login_data: LoginData
    post_count: PostCounter

    def get_simple_user(self):
        return SimpleUser(
            user_account=self.user_account,
            nickname=self.nickname,
            uid=self.uid,
            auth=self.auth,
        )


class FullUesrAction(SecurityUesrAction):
    name: str

    def get_user_name(self) -> str:
        return self.name


@dataclass
class User(FullUesrAction):
    pw: Password
    user_account: UserId
    name: str
    nickname: str
    auth: AuthArchives
    login_data: LoginData
    post_count: PostCounter
    uid: Optional[Uid] = None

    def get_passwd(self) -> str:
        return self.pw.pw

    def get_uid(self) -> Optional[Uid]:
        return self.uid


@dataclass(frozen=True)
class UserVO(FullUesrAction):
    user_account: UserId
    name: str
    nickname: str
    uid: Uid
    auth: AuthArchives
    login_data: LoginData
    post_count: PostCounter

    def get_simple_user(self):
        return SimpleUser(
            user_account=self.user_account,
            nickname=self.nickname,
            uid=self.uid,
            auth=self.auth,
            post_count=self.post_count,
        )

    def get_security_simple_user(self):
        return SecuritySimpleUser(
            user_account=self.user_account,
            nickname=self.nickname,
            uid=self.uid,
            auth=self.auth,
            post_count=self.post_count,
            login_data=self.login_data,
        )
