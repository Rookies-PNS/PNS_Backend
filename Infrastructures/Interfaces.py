from abc import *


class IMigrations(metaclass=ABCMeta):
    @abstractmethod
    def create_user(self):
        ...

    @abstractmethod
    def init_user(self):
        ...

    @abstractmethod
    def create_post(self):
        ...

    @abstractmethod
    def init_post(self):
        ...


from Applications.Repositories.Interfaces import IPostRepository, IUserRepository


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
