import __init__
from abc import *
from typing import Optional

from Commons import PostId
from Domains.Entities import Post, PostVO, SimplePost
from Applications.Results import Result, Fail


class IPostRepository(metaclass=ABCMeta):
    @abstractmethod
    def check_exist_pid(self, post_id: PostId) -> bool:
        """_summary_
        일기의 존재 여부를 판단한다.

        Args:
            post_id (PostId): _description_

        Returns:
            bool: _description_
        """
        pass

    @abstractmethod
    def save(self, post: Post) -> Optional[Fail]:
        """_summary_
        일기를 저장한다.

        Args:
            post (Post): _description_

        Returns:
            Optional[Fail]: _description_
        """
        pass

    @abstractmethod
    def update_all(self, post: PostVO) -> Result[PostId]:
        """_summary_
        일기 내용 전부를 수정한다.

        Args:
            post (PostVO): _description_

        Returns:
            Result[PostId]: _description_
        """
        pass

    @abstractmethod
    def update_share(self, post: SimplePost) -> Result[PostId]:
        """_summary_
        일기의 공유설정을 변경한다.

        Args:
            post (SimplePost): _description_

        Returns:
            Result[PostId]: _description_
        """
        pass

    @abstractmethod
    def delete(self, post: PostVO) -> Result[PostId]:
        """_summary_
        일기를 삭제한다.

        Args:
            post (PostVO): _description_

        Returns:
            Result[PostId]: _description_
        """
        pass
