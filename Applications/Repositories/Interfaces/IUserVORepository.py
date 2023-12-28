import __init__
from typing import Optional
from abc import *

from Commons import Uid, UserId, Password
from Domains.Entities import User, UserVO, SimpleUser
from Applications.Results import Result


class IUserVORepository(metaclass=ABCMeta):
    @abstractmethod
    def check_exist_userid(self, userid: str) -> bool:
        """_summary_
        userid를 통해서 저장소에 존재하는지 여부를 알 수 있다.

        Args:
            userid (str): _description_

        Returns:
            bool: _description_
        """
        pass

    @abstractmethod
    def search_by_uid(self, uid: Uid) -> Optional[UserVO]:
        """_summary_
        uid를 통해서 유저의 모든 정보를 알 수 있다.

        Args:
            uid (Uid): _description_

        Returns:
            Optional[UserVO]: _description_
        """
        pass

    @abstractmethod
    def search_by_userid(self, userid: UserId) -> Optional[SimpleUser]:
        """_summary_
        계정을 통해 유저를 조회한다.

        Args:
            userid (UserId): _description_

        Returns:
            Optional[SimpleUser]: _description_
        """
        pass

    @abstractmethod
    def compare_pw(self, user: SimpleUser, pw: Password) -> bool:
        """_summary_
        유저의 패스워드를 비교해서 결과를 반환해 준다.

        Args:
            user (SimpleUser): _description_
            pw (Password): _description_

        Returns:
            bool: _description_
        """
        pass
