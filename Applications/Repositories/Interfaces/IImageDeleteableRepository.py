import __init__
from abc import *
from typing import Optional

from Commons import ImageKey
from Applications.Results import Result, Fail


class IImageDeleteableRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def check_exist_key(self, key: ImageKey) -> Result[bool]:
        pass

    @abstractclassmethod
    def delete_image_data(self, key: ImageKey) -> Optional[Fail]:
        pass

    @abstractclassmethod
    def check_exist_image(self, key: ImageKey) -> bool:
        pass
