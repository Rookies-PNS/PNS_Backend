import __init__
from dataclasses import dataclass
from datetime import datetime
from Commons import UpdateableTime


@dataclass
class PostCounter:
    last_update_date: UpdateableTime
    post_num: int = 0

    def count_post_num(self):
        """
        현재 날짜와 last_update_date를 비교하여 게시물 수를 업데이트하는 메서드
        """

        # 현재 날짜와 last_update_date를 비교하여 업데이트 여부 결정
        if datetime.now().date() == self.last_update_date.get_time().date():
            self.post_num += 1
        else:
            self.post_num = 1
        self.last_update_date.set_now()

    def get_post_num(self) -> int:
        """
        게시물 수를 반환하는 메서드
        """
        if datetime.now().date() != self.last_update_date.get_time().date():
            return 0
        else:
            return self.post_num
