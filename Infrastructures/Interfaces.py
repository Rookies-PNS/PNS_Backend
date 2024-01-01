from abc import *
from collections.abc import Collection

from Domains.Entities import UserVO, PostVO
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IPostReadableRepository,
    IUserWriteableRepository,
    IUserReadableRepository,
    IMigrations,
    IImageReadableRepository,
    IImageWriteableRepository,
)


class IStorageFactory(metaclass=ABCMeta):
    @abstractmethod
    def get_migrations(self) -> IMigrations:
        pass

    @abstractmethod
    def get_user_write_storage(self) -> IUserWriteableRepository:
        pass

    @abstractmethod
    def get_user_read_storage(self) -> IUserReadableRepository:
        pass

    @abstractmethod
    def get_post_write_storage(self) -> IPostWriteableRepository:
        pass

    @abstractmethod
    def get_post_read_storage(self) -> IPostReadableRepository:
        pass

    @abstractclassmethod
    def get_image_read_storage(self) -> IImageReadableRepository:
        pass

    @abstractclassmethod
    def get_image_write_storage(self) -> IImageWriteableRepository:
        pass
