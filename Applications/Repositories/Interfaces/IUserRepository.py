import __init__
from typing import Optional
from abc import *

from Commons import Uid, UserId
from Domains.Entities import User, UserVO, SimpleUser
from Applications.Results import Result


class IUserRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def check_exist_userid(self, userid: str) -> bool:
        pass

    @abstractclassmethod
    def save(self, user: User) -> Result[SimpleUser]:
        pass

    @abstractclassmethod
    def search_by_uid(self, uid: Uid) -> Optional[UserVO]:
        pass

    @abstractclassmethod
    def search_by_userid(self, userid: UserId) -> Optional[UserVO]:
        pass

    @abstractclassmethod
    def update(self, user: UserVO) -> Result[SimpleUser]:
        pass

    @abstractmethod
    def delete(self, user: UserVO) -> Result[Uid]:
        pass
