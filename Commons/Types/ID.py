import dataclasses


@dataclasses.dataclass(frozen=True)
class ID:
    id: int


@dataclasses.dataclass(frozen=True)
class UserID(ID):
    ...


@dataclasses.dataclass(frozen=True)
class PostID(ID):
    ...
