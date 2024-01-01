import __init__
from abc import *
from typing import Optional

from Commons import ImageKey, Uid
from Domains.Entities import ImageData, PostVO
from Applications.Results import Result, Fail


class IImageWriteableRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def check_exist_key(self, key: ImageKey) -> Result[bool]:
        pass

    @abstractclassmethod
    def upload_to_s3(file, bucket_name, object_name) -> Optional[Fail]:
        """_summary_
        s3클라이언트를 생성하고 파일 객체를 s3버킷에
        업로드 합니다.

        Args:
            file (_type_): 이미지의 소유권을 나타낸다.
            bucket_name: 버킷 이름
            object_name : 버킷에 저장되는 파일 이름
        Returns:
            Optional[Fail]: _description_
        """
        pass

    @abstractclassmethod
    def save_image_data(self, uid: Uid, s3_url) -> Result[ImageKey]:
        """_summary_
        그이후 ImageData를 생성하여 DB에 저장한다.

        Args:
            uid (Uid): 이미지의 소유권을 나타낸다.
            img (_type_): 저장하고 싶은 이미지

        Returns:
            Result[ImageKey]: 이미지 접근할 수 있는 Key
        """
        pass

    @abstractclassmethod
    def delete_image(self, key: ImageKey) -> Optional[Fail]:
        """_summary_
        이미지를 저장소에서 삭제하고, DB에 남아있는 데이터도 삭제한다.
        Args:
            key (ImageKey): Key를 사용해서 이미지에 접근

        Returns:
            Optional[Fail]: _description_
        """
        pass

    @abstractclassmethod
    def check_exist_image(self, key: ImageKey) -> bool:
        pass
