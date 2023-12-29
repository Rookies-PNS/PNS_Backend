import __init__

from Infrastructures.IOC import get_strage_factory, select_table_name_padding
from Infrastructures.Interfaces import IMigrations, IStorageFactory
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IUserWriteableRepository,
)


def get_test_factory(padding: str = "user_service_test_") -> IStorageFactory:
    select_table_name_padding(padding)

    return get_strage_factory()


def get_usecase_migration(factory: IStorageFactory) -> IMigrations:
    return factory.get_migrations()


def get_post_storage(factory: IStorageFactory) -> IPostWriteableRepository:
    return factory.get_post_strage()


def get_user_storage(factory: IStorageFactory) -> IUserWriteableRepository:
    return factory.get_user_strage()
