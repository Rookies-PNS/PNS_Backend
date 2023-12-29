import __init__
from typing import Optional
from abc import *

from Commons import Uid, UserId
from Domains.Entities import User, UserVO, SimpleUser, SecuritySimpleUser
from Applications.Results import Result, Fail


class IUserWriteableRepository(metaclass=ABCMeta):
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
    def save_user(self, user: User) -> Optional[Fail]:
        """_summary_
        사용자를 저장한다.

        Args:
            user (User): _description_

        Returns:
            Optional[Fail]: 성공시 None 반환, 실패시 Fail반환
        """
        pass

    @abstractclassmethod
    def update_all(self, user: UserVO) -> Optional[Fail]:
        """_summary_
        사용자 정보를 갱신한다.

        Args:
            user (UserVO): _description_

        Returns:
            Result[Uid]: _description_
        """
        pass

    @abstractclassmethod
    def update_auth(self, user: SecuritySimpleUser) -> Optional[Fail]:
        """_summary_
        사용자의 권한정보를 갱신한다.

        Args:
            user (SimpleUser): _description_

        Returns
            Optional[Fail]: None 이면 성공, Fail이면 실패
        """
        pass

    @abstractclassmethod
    def update_post_counter(self, user: SimpleUser) -> Result[int]:
        """_summary_
        사용자의 마지막 일기 수정일 갱신과 마지막날 작성한 일기의 개수를 카운트 한다.
        현재 날짜와 수정일이 같으면 카운트는 증가하고,
        현재 날짜와 수정일이 다르면 카운트는 1로 수정일은 현재 날짜로 갱신된다.

        Args:
            user (SimpleUser): _description_

        Returns:
            Result[int]: 당일 일기 작성 개수
        """
        pass

    @abstractclassmethod
    def update_to_fail_login(self, user: SimpleUser) -> Result[int]:
        """_summary_
        로그인을 실패한 것으로 업데이트 한다.

        Args:
            user (SimpleUser): _description_

        Returns:
            Result[int]: 로그인 실패 횟수
        """
        pass

    @abstractclassmethod
    def update_to_success_login(self, user: SimpleUser) -> Optional[Fail]:
        """_summary_
        로그인을 성공한 것으로 업데이트 한다.

        Args:
            user (SimpleUser): _description_

        Returns:
            Optional[Fail]: None 이면 성공, Fail이면 실패
        """
        pass

    @abstractclassmethod
    def delete(self, user: SimpleUser) -> Result[Uid]:
        """_summary_
        사용자의 정보를 삭제(비공개) 처리한다.

        Args:
            user (SimpleUser): _description_

        Returns:
            Result[Uid]: _description_
        """
        pass
