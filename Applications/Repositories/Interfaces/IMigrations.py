from abc import *
from collections.abc import Collection

from Domains.Entities import UserVO, PostVO


class IMigrations(metaclass=ABCMeta):
    @abstractmethod
    def create_user(self):
        ...

    @abstractmethod
    def delete_user(self):
        ...

    @abstractmethod
    def check_exist_user(self) -> bool:
        ...

    @abstractmethod
    def create_post(self):
        ...

    @abstractmethod
    def delete_post(self):
        ...

    @abstractmethod
    def check_exist_post(self) -> bool:
        ...
