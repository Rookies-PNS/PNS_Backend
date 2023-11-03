import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class Id:
    idx: int


@dataclasses.dataclass(frozen=True)
class Uid(Id):
    ...


@dataclasses.dataclass
class UserId:
    uid: Optional[Uid]
    id: str


@dataclasses.dataclass(frozen=True)
class UserIdVO:
    uid: Uid
    id: str


@dataclasses.dataclass(frozen=True)
class PostId(Id):
    ...
