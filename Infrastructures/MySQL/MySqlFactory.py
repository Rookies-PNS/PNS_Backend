import __init__

from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IUserWriteableRepository,
)

from Infrastructures.Interfaces import IStorageFactory, IMigrations


class MySqlFactory(IStorageFactory):
    def __init__(self, name_padding: str = "log") -> None:
        self.padding = name_padding

    def get_migrations(self) -> IMigrations:
        from Infrastructures.MySQL.Storages.MySqlMigrations import MySqlMigrations

        return MySqlMigrations(self.padding)

    def get_user_strage(self) -> IUserWriteableRepository:
        from Infrastructures.MySQL.Storages.MySqlUserStorage import MySqlUserStorage

        return MySqlUserStorage(self.padding)

    def get_post_strage(self) -> IPostWriteableRepository:
        from Infrastructures.MySQL.Storages.MySqlPostStorage import MySqlPostStorage

        return MySqlPostStorage(self.get_user_strage(), self.padding)
