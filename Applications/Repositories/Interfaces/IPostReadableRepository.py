import __init__
from typing import Optional
from collections.abc import Collection
from abc import *

from Commons import Uid, PostId
from Domains.Entities import PostVO, SimplePost
from Applications.Results import Result


class IPostReadableRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def check_exist_pid(self, post_id: PostId) -> bool:
        """_summary_
        일기의 존재여부를 확인한다.

        Args:
            post_id (PostId): _description_

        Returns:
            bool: _description_
        """
        pass

    @abstractclassmethod
    def get_num_of_public_post(self) -> int:
        """_summary_
        공유 일기의 개수를 확인한다.

        Returns:
            int: _description_
        """
        pass

    @abstractclassmethod
    def get_public_post_list(
        self,
        page: int = 0,
        posts_per_page: Optional[int] = None,
    ) -> Result[Collection[SimplePost]]:
        """_summary_
        공유 일기 리스트를 받아온다.

        Args:
            page (int, optional): _description_. Defaults to 0.
            posts_per_page (Optional[int], optional): 한번에 가져올 일기의 개수 정의, None은 모든 요소를 가져온다. Defaults to None.

        Returns:
            Result[Collection[SimplePost]]: _description_
        """
        pass

    @abstractclassmethod
    def search_by_pid(self, post_id: PostId) -> Optional[PostVO]:
        """_summary_
        pid를 기준으로 일기를 검색한다.

        Args:
            post_id (PostId): _description_

        Returns:
            Optional[PostVO]: _description_
        """
        pass

    @abstractclassmethod
    def get_num_of_post_search_by_available_uid(self, user_id: Uid) -> int:
        """_summary_
        uid가 보유중인 사용가능한 일기의 개수를 가져온다.

        Args:
            user_id (Uid): _description_

        Returns:
            int: _description_
        """
        pass

    @abstractclassmethod
    def search_by_available_uid(
        self,
        user_id: Uid,
        page: int = 0,
        posts_per_page: Optional[int] = None,
    ) -> Result[Collection[SimplePost]]:
        """_summary_
        uid를 기준으로 검색한다.
        단 삭제 플레그가 없는 사용가능한 일기만 가져온다.

        Args:
            user_id (Uid): _description_
            page (int, optional): _description_. Defaults to 0.
            posts_per_page (Optional[int], optional): 한번에 가져올 일기의 개수 정의, None은 모든 요소를 가져온다. Defaults to None.

        Returns:
            Result[Collection[SimplePost]]: _description_
        """
        pass

    @abstractclassmethod
    def search_by_uid(
        self,
        user_id: Uid,
    ) -> Result[Collection[SimplePost]]:
        """_summary_
        uid를 기준으로 모든 일기를 가져온다.

        Args:
            user_id (Uid): _description_

        Returns:
            Result[Collection[SimplePost]]: _description_
        """
        pass
