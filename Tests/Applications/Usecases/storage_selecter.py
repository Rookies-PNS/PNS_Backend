import __init__
from typing import Tuple

from Infrastructures.IOC import get_strage_factory, select_table_name_padding
from Infrastructures.Interfaces import IMigrations, IStorageFactory
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IPostReadableRepository,
    IUserWriteableRepository,
    IUserReadableRepository,
    SessionRepository,
)


def get_test_factory(padding: str = "user_service_test_") -> IStorageFactory:
    select_table_name_padding(padding)

    return get_strage_factory()


def get_usecase_migration(factory: IStorageFactory) -> IMigrations:
    return factory.get_migrations()


def get_post_storage(
    factory: IStorageFactory,
) -> Tuple[IPostWriteableRepository, IPostReadableRepository]:
    return factory.get_post_write_storage(), factory.get_post_read_storage()


def get_user_storage(
    factory: IStorageFactory,
) -> Tuple[IUserWriteableRepository, IUserReadableRepository]:
    return factory.get_user_write_storage(), factory.get_user_read_storage()


def get_session_storage(factory: IStorageFactory) -> SessionRepository:
    return factory.get_session_storage()
