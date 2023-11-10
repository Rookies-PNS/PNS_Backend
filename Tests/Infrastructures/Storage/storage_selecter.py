import __init__

from Infrastructures.IOC import get_strage_factory, select_table_name_padding
from Infrastructures.Interfaces import IMigrations, IStorageFactory
from Applications.Repositories.Interfaces import IPostRepository, IUserRepository


def get_storage_migration(padding: str = "test_") -> IMigrations:
    select_table_name_padding(padding)
    f = get_strage_factory()
    return f.get_migrations()
