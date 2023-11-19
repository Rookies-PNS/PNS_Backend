import dataclasses
from datetime import datetime


def get_current_time() -> datetime:
    return datetime.now()


@dataclasses.dataclass(frozen=True)
class PostCreateTime:
    time: datetime

    def get_time(self) -> datetime:
        return self.time


@dataclasses.dataclass
class PostUpdateTime:
    time: datetime

    def set_time(self):
        self.time = get_current_time()

    def get_time(self) -> datetime:
        return self.time
