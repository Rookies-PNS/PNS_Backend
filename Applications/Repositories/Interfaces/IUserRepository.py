import __init__
from typing import Optional
from abc import *

from Commons import Uid, UserId
from Domains.Models import User, UserVO
from Applications.Results import Result


class IUserRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def check_not_exist_userid(self, userid: str) -> Result[UserId]:
        pass

    @abstractclassmethod
    def save(self, user: User) -> Result[UserVO]:
        pass

    @abstractclassmethod
    def search_by_uid(self, uid: Uid) -> Optional[UserVO]:
        pass

    @abstractclassmethod
    def search_by_userid(self, userid: UserId) -> Optional[UserVO]:
        pass

    @abstractclassmethod
    def update(self, user: UserVO) -> Result[UserVO]:
        pass

    @abstractmethod
    def delete(self, user: UserVO) -> Result[Uid]:
        pass
