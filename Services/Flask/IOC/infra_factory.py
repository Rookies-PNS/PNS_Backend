import __init__

from Applications.Usecases import LoginUser
from Applications.Repositories.Interfaces import IUserRepository, IPostRepository


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
