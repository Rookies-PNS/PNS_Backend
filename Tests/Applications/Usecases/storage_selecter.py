import __init__

from Infrastructures.IOC import get_strage_factory
from Infrastructures.Interfaces import IMigrations, IStorageFactory
from Applications.Repositories.Interfaces import IPostRepository, IUserRepository


def get_usecase_migration(padding: str = "user_service_test_") -> IMigrations:
    f = get_strage_factory(padding)
    return f.get_migrations()


def get_post_storage(padding: str = "user_service_test_") -> IPostRepository:
    f = get_strage_factory(padding)
    return f.get_post_strage()


def get_user_storage(padding: str = "user_service_test_") -> IUserRepository:
    f = get_strage_factory(padding)
    return f.get_user_strage()
