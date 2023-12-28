from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from Commons import UpdateableTime


@dataclass
class LoginData:
    lock_time: UpdateableTime
    lock_flag: bool = False
    count_of_login_fail: int = 0

    def get_count_of_login_fail(self) -> int:
        return self.count_of_login_fail

    def get_due_to_of_login_lock(self) -> datetime:
        return self.lock_time.get_time()

    def check_login_able(self) -> bool:
        """
        로그인 가능 여부를 확인하는 함수
        """
        # 계정이 잠겨 있으면 로그인 불가능
        if self.lock_flag:
            # 잠긴 상태에서 시간이 지난 경우 잠금 해제
            if self.lock_time.compare_time(datetime.now()):
                self.lock_flag = False
                return True
            else:
                return False

        # 그 외에는 로그인 가능
        return True

    def fail_login(self):
        self.count_of_login_fail += 1

    def success_login(self):
        self.lock_flag = False
        self.count_of_login_fail = 0

    def lock_login(self, time_minute: int):
        self.lock_time.set_minute(time_minute)
        self.lock_flag = True
