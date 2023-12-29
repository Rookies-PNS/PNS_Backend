from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta


def get_current_time() -> datetime:
    return datetime.now()


class TIME:
    def get_time(self) -> datetime:
        return self.time

    def compare_time(self, time: datetime) -> bool:
        """_summary_
        입력된 결과를 비교한다.

        Args:
            time (datetime): 비교대상 시간

        Returns:
            bool: 비교대상이 클 경우 참 반환, 나머지는 거짓 반환
        """
        return self.time < time


@dataclass(frozen=True)
class TimeVO(TIME):
    time: datetime


@dataclass
class UpdateableTime(TIME):
    time: datetime

    def set_now(self):
        self.time = get_current_time()

    def set_minute(self, time: int):
        self.time = get_current_time() + timedelta(minutes=time)


@dataclass
class SelectTime(UpdateableTime):
    def set_time(self, time: datetime):
        self.time = time
