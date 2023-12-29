import __init__
from abc import *
from typing import Optional

from Commons import ImageKey
from Domains.Entities import ImageData, PostVO
from Applications.Results import Result, Fail


class IImageSaveableRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def check_exist_key(self, key: ImageKey) -> Result[bool]:
        pass

    @abstractclassmethod
    def save_image(self, post: PostVO, img) -> Result[ImageData]:
        pass
