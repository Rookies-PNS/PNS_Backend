from dataclasses import dataclass


@dataclass(frozen=True)
class Id:
    idx: int


@dataclass(frozen=True)
class Uid(Id):
    ...


@dataclass
class UserId:
    account: str


@dataclass(frozen=True)
class PostId(Id):
    ...


@dataclass(frozen=True)
class ImageKey:
    """_summary_
    Args:
        access_key : 이미지에 접근할 수 있는 url 키
    """

    access_key: str

    def get_image_access_key(self) -> str:
        return self.access_key
