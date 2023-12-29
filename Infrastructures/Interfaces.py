from abc import *
from collections.abc import Collection

from Domains.Entities import UserVO, PostVO
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IUserWriteableRepository,
    IMigrations,
)


class IStorageFactory(metaclass=ABCMeta):
    @abstractmethod
    def get_migrations(self) -> IMigrations:
        pass

    @abstractmethod
    def get_user_strage(self) -> IUserWriteableRepository:
        pass

    @abstractmethod
    def get_post_strage(self) -> IPostWriteableRepository:
        pass
