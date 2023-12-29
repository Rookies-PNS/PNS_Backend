from dataclasses import dataclass
from Commons import Uid, PostId, ImageKey


@dataclass(frozen=True)
class ImageData(ImageKey):
    """_summary_
    Args:
        access_key : 이미지에 접근할 수 있는 url 키
        thumbnail_path : 썸네일 이미지가 저장된 장소
        origin_path : 원본이미지가 저장된 장소
        owner : owner
        post : linked post
    """

    access_key: ImageKey
    thumbnail_path: str
    origin_path: str
    owner: Uid
    post: PostId

    def get_image_access_key(self) -> str:
        return self.access_key.get_image_access_key()
