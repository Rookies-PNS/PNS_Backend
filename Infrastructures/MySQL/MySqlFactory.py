import __init__

from Applications.Repositories.Interfaces import IPostRepository, IUserRepository

from Infrastructures import IStorageFactory, IMigrations


class MySqlFactory(IStorageFactory):
    def get_migrations(self) -> IMigrations:
        from Infrastructures.MySQL.Storages.MySqlMigrations import MySqlMigrations

        return MySqlMigrations()

    def get_user_strage(self) -> IUserRepository:
        from Infrastructures.MySQL.Storages.MySqlUserStorage import MySqlUserStorage

        return MySqlUserStorage()

    def get_post_strage(self) -> IPostRepository:
        from Infrastructures.MySQL.Storages.MySqlPostStorage import MySqlPostStorage

        return MySqlPostStorage()
