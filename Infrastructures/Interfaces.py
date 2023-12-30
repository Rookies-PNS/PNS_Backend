from abc import *
from collections.abc import Collection

from Domains.Entities import UserVO, PostVO
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IPostReadableRepository,
    IUserWriteableRepository,
    IUserReadableRepository,
    IMigrations,
    IImageDataReadableRepository,
    IImageDeleteableRepository,
    IImageSaveableRepository,
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
    def get_image_data_read_storage(self) -> IImageDataReadableRepository:
        pass

    @abstractclassmethod
    def get_image_save_storage(self) -> IImageDeleteableRepository:
        pass

    @abstractclassmethod
    def get_image_delete_storage(self) -> IImageSaveableRepository:
        pass
