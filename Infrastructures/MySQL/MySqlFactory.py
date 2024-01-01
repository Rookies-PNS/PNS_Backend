import __init__

from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IPostReadableRepository,
    IUserWriteableRepository,
    IUserReadableRepository,
    IMigrations,
    IImageReadableRepository,
    IImageWriteableRepository,
)

from Infrastructures.Interfaces import IStorageFactory, IMigrations


class MySqlFactory(IStorageFactory):
    def __init__(self, name_padding: str = "log") -> None:
        self.padding = name_padding

    def get_migrations(self) -> IMigrations:
        from Infrastructures.MySQL.Storages.MySqlMigrations import MySqlMigrations

        return MySqlMigrations(self.padding)

    def get_user_write_storage(self) -> IUserWriteableRepository:
        from Infrastructures.MySQL.Storages.MySqlUserWriteStorage import (
            MySqlUserWriteStorage,
        )

        return MySqlUserWriteStorage(self.padding)

    def get_user_read_storage(self) -> IUserReadableRepository:
        from Infrastructures.MySQL.Storages.MySqlUserReadStorage import (
            MySqlUserReadStorage,
        )

        return MySqlUserReadStorage(self.padding)

    def get_post_write_storage(self) -> IPostWriteableRepository:
        from Infrastructures.MySQL.Storages.MySqlPostWriteStorage import (
            MySqlPostWriteStorage,
        )

        return MySqlPostWriteStorage(self.get_user_read_storage(), self.padding)

    def get_post_read_storage(self) -> IPostReadableRepository:
        from Infrastructures.MySQL.Storages.MySqlPostWriteStorage import (
            MySqlPostWriteStorage,
        )

        return MySqlPostWriteStorage(self.get_user_read_storage(), self.padding)

    def get_image_read_storage(self) -> IImageReadableRepository:
        raise NotImplementedError()

    def get_image_write_storage(self) -> IImageWriteableRepository:
        raise NotImplementedError()
