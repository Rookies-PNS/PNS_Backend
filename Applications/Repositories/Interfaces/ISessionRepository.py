import __init__
from typing import Optional
from abc import *

from Commons import Uid
from Domains.Entities import UserSession, SimpleUser
from Applications.Results import Result, Fail


class ISessionRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def save_session(self, session: UserSession) -> Optional[Fail]:
        pass

    @abstractclassmethod
    def session_to_user(self, session_key: str) -> Optional[SimpleUser]:
        pass

    @abstractclassmethod
    def delete_session(self, uid: Uid) -> Optional[Fail]:
        pass
