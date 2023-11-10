import __init__

from Infrastructures.IOC import get_strage_factory, select_table_name_padding
from Infrastructures.Interfaces import IMigrations, IStorageFactory
from Applications.Repositories.Interfaces import IPostRepository, IUserRepository


def get_usecase_migration(padding: str = "user_service_test_") -> IMigrations:
    select_table_name_padding(padding)

    f = get_strage_factory()
    return f.get_migrations()


def get_post_storage(padding: str = "user_service_test_") -> IPostRepository:
    select_table_name_padding(padding)
    f = get_strage_factory()
    return f.get_post_strage()


def get_user_storage(padding: str = "user_service_test_") -> IUserRepository:
    select_table_name_padding(padding)
    f = get_strage_factory()
    return f.get_user_strage()
