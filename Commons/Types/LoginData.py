from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta
from Commons import UpdateableTime


@dataclass
class LoginData:
    time_of_try_login: UpdateableTime
    lock_flag: bool = False
    count_of_login_fail: int = 0

    def get_count_of_login_fail(self) -> int:
        return self.count_of_login_fail

    def get_due_to_of_login_lock(self) -> datetime:
        return self.time_of_try_login.get_time()

    def check_login_able(self, block_minute: int) -> bool:
        """
        로그인 가능 여부를 확인하는 함수
        """
        # 계정이 잠겨 있으면 로그인 불가능
        if self.lock_flag:
            # 잠긴 상태에서 시간이 지난 경우 잠금 해제
            if self.time_of_try_login.compare_time(
                datetime.now() - timedelta(minutes=block_minute)
            ):
                self.lock_flag = False
                return True
            else:
                return False

        # 그 외에는 로그인 가능
        return True

    def fail_login(self):
        self.count_of_login_fail += 1
        self.time_of_try_login.set_now()

    def success_login(self):
        self.lock_flag = False
        self.count_of_login_fail = 0
        self.time_of_try_login.set_now()

    def lock_login(self):
        self.lock_flag = True
