import __init__
from abc import *
from typing import Optional

from Commons import ImageKey
from Domains.Entities import ImageData
from Applications.Results import Result


class IImageReadableRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def check_exist_key(self, key: ImageKey) -> Result[bool]:
        pass

    @abstractclassmethod
    def check_exist_image(self, key: ImageKey) -> bool:
        pass

    @abstractclassmethod
    def get_image_data(self, key: ImageKey) -> Result[ImageData]:
        pass
