import dataclasses


@dataclasses.dataclass(frozen=True)
class Id:
    idx: int


@dataclasses.dataclass(frozen=True)
class Uid(Id):
    ...


@dataclasses.dataclass
class UserId:
    account: str


@dataclasses.dataclass(frozen=True)
class PostId(Id):
    ...
