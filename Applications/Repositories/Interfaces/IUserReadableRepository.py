import __init__
from collections.abc import Collection
from typing import Optional
from abc import *

from Commons import Uid, UserId, Password, LoginData
from Domains.Entities import SecuritySimpleUser, UserVO, SimpleUser
from Applications.Results import Result


class IUserReadableRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def check_exist_userid(self, userid: str) -> bool:
        """_summary_
        userid를 통해서 저장소에 존재하는지 여부를 알 수 있다.

        Args:
            userid (str): _description_

        Returns:
            bool: _description_
        """
        pass

    @abstractclassmethod
    def search_by_uid(self, uid: Uid) -> Optional[UserVO]:
        """_summary_
        uid를 통해서 유저의 모든 정보를 알 수 있다.

        Args:
            uid (Uid): _description_

        Returns:
            Optional[UserVO]: _description_
        """
        pass

    @abstractclassmethod
    def search_by_userid(self, userid: UserId) -> Optional[SimpleUser]:
        """_summary_
        계정을 통해 유저를 조회한다.

        Args:
            userid (UserId): _description_

        Returns:
            Optional[SimpleUser]: _description_
        """
        pass

    @abstractclassmethod
    def get_num_of_security_user(self) -> int:
        """_summary_
        유효한 시큐리티 사용자 계정의 총 수를 반환합니다.
        Returns:
            int: 검색된 인원수
        """
        pass

    @abstractclassmethod
    def get_security_user_list(
        self,
        page: int = 0,
        posts_per_page: Optional[int] = None,
    ) -> Result[Collection[SecuritySimpleUser]]:
        """_summary_


        Args:
            user_id (Uid): _description_
            page (int, optional): _description_. Defaults to 0.
            posts_per_page (Optional[int], optional): 한번에 가져올 일기의 개수 정의, None은 모든 요소를 가져온다. Defaults to None.

        Returns:
            Result[Collection[SimplePost]]: _description_
        """
        pass

    @abstractclassmethod
    def get_login_data(self, user_id: UserId) -> Result[LoginData]:
        """_summary_
        사용자의 로그인 실패 현황을 받아온다.

        Args:
            user_id (UserId): _description_

        Returns:
            Result[LoginData]: _description_
        """
        pass

    @abstractclassmethod
    def compare_pw(self, user_id: UserId, pw: Password) -> bool:
        """_summary_
        유저의 패스워드를 비교해서 결과를 반환해 준다.

        Args:
            user (SimpleUser): _description_
            pw (Password): _description_

        Returns:
            bool: _description_
        """
        pass
