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
    Auth,
)


class CommonUserAction:
    user_id: UserId
    nickname: str
    uid: Uid
    auth: AuthArchives
    login_data: LoginData
    post_count: PostCounter

    def get_account(self) -> str:
        return self.user_id.account

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

    def get_count_of_login_fail(self) -> int:
        return self.login_data.get_count_of_login_fail()

    def get_due_to_of_login_lock(self) -> datetime:
        return self.login_data.get_due_to_of_login_lock()

    def check_login_able(self) -> bool:
        """
        로그인 가능 여부를 확인하는 함수
        """
        return self.login_data.check_login_able()

    def fail_login(self):
        return self.login_data.fail_login()

    def success_login(self):
        return self.login_data.success_login()

    def lock_login(self, time_minute: int):
        return self.login_data.lock_login(time_minute)

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

    def check_get_auth(self, auth: Auth) -> bool:
        """
        auth(인자)권한을 소유하고 있는지를 반환한다.
        Args:
            auth (Auth):확인하고 싶은 권한을 넣는다.

        Returns:
            bool: True(해당 권한을 가짐), False(권한 없음)
        """
        return self.auth.check_get_auth(auth)


@dataclass(frozen=True)
class SimpleUser(CommonUserAction):
    user_id: UserId
    nickname: str
    uid: Uid
    auth: AuthArchives
    login_data: LoginData
    post_count: PostCounter


class FullUesrAction(CommonUserAction):
    name: str

    def get_user_name(self) -> str:
        return self.name


@dataclass
class User(FullUesrAction):
    pw: Password
    user_id: UserId
    name: str
    nickname: str
    auth: AuthArchives
    login_data: LoginData
    post_count: PostCounter
    uid: Optional[Uid] = None

    def get_passwd(self) -> str:
        return self.pw.pw


@dataclass(frozen=True)
class UserVO(FullUesrAction):
    user_id: UserId
    name: str
    nickname: str
    uid: Uid
    auth: AuthArchives
    login_data: LoginData
    post_count: PostCounter

    def get_simple_user(self):
        return SimpleUser(
            user_id=self.user_id,
            nickname=self.nickname,
            uid=self.uid,
            auth=self.auth,
            login_data=self.login_data,
        )
