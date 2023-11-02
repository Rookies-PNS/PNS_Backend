import dataclasses


@dataclasses.dataclass
class ID:
    id: int


@dataclasses.dataclass
class UserID:
    id: ID


@dataclasses.dataclass
class PostID:
    id: ID
