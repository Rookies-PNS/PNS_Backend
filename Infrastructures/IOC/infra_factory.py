import __init__

from Applications.Usecases import LoginUser
from Applications.Repositories.Interfaces import IUserRepository, IPostRepository

from Infrastructures.Interfaces import IStorageFactory

storage_type = "mysql"
padding = "log_"


def select_strage(type: str):
    global storage_type
    match type.lower():
        case "mysql":
            storage_type = type
        case _:
            raise ValueError(
                f"""
ValueError  > Possible inputs are 'mysql'
            > your input : {storage_type}"""
            )


def select_table_name_padding(table_name_padding: str = "log_"):
    global padding
    padding = table_name_padding


def get_strage_factory() -> IStorageFactory:
    from Infrastructures.MySQL import MySqlFactory

    global padding

    global storage_type

    match storage_type:
        case "mysql":
            return MySqlFactory(padding)
        case _:
            raise ValueError(
                f"""
ValueError  > Possible inputs are 'mysql'
            > your input : {storage_type}
"""
            )


def get_user_storage() -> IUserRepository:
    global padding

    f = get_strage_factory()
    return f.get_user_strage()
