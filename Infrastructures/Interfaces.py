from abc import *
from collections.abc import Collection

from Domains.Entities import UserVO, PostVO
from Applications.Repositories.Interfaces import (
    IPostRepository,
    IUserRepository,
    IMigrations,
)


class IStorageFactory(metaclass=ABCMeta):
    @abstractmethod
    def get_migrations(self) -> IMigrations:
        pass

    @abstractmethod
    def get_user_strage(self) -> IUserRepository:
        pass

    @abstractmethod
    def get_post_strage(self) -> IPostRepository:
        pass
