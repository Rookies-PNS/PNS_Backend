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
    id: str


@dataclasses.dataclass(frozen=True)
class PostId(Id):
    ...
