import __init__

from Applications.Usecases import LoginUser
from Applications.Repositories.Interfaces import IUserRepository, IPostRepository

from Infrastructures.Interfaces import IStorageFactory


def get_user_storage() -> IUserRepository:
    from Tests.Applications.Implements.test_user_repository_list import (
        TestUserRepositoryList,
    )
    from Domains.Entities import UserVO
    from Commons import UserId, Uid, Password

    repo = TestUserRepositoryList(
        [UserVO(UserId(id="aaa"), "admin", Password(pw="aaa"), Uid(idx=1))]
    )
    return repo


storage_type = "mysql"


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


def get_strage_factory(name_padding: str = "log") -> IStorageFactory:
    from Infrastructures.MySQL import MySqlFactory

    global storage_type

    match storage_type:
        case "mysql":
            return MySqlFactory(name_padding)
        case _:
            raise ValueError(
                f"""
ValueError  > Possible inputs are 'mysql'
            > your input : {storage_type}"""
            )
