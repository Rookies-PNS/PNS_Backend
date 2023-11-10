import __init__

from Infrastructures.IOC import get_strage_factory
from Infrastructures.Interfaces import IMigrations, IStorageFactory
from Applications.Repositories.Interfaces import IPostRepository, IUserRepository


def get_storage_migration(padding: str = "test_") -> IMigrations:
    f = get_strage_factory(padding)
    return f.get_migrations()
