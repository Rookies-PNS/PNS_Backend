import __init__
from typing import Optional
from collections.abc import Collection
from abc import *

from Commons import Uid, PostId
from Domains.Entities import Post, PostVO, SimplePost
from Applications.Results import Result
from Applications.Repositories.Queries import IPostQuery


class IPostRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def save(self, post: Post) -> Result[SimplePost]:
        pass

    @abstractclassmethod
    def get_post_per_page_list(
        self,
        page: Optional[int] = None,
        posts_per_page: Optional[int] = None,
    ) -> Collection[SimplePost]:
        pass

    @abstractclassmethod
    def search_by_uid(self, post_id: PostId) -> Optional[PostVO]:
        pass

    @abstractclassmethod
    def search_by_query(self, query: IPostQuery) -> Collection[SimplePost]:
        pass

    @abstractclassmethod
    def update(self, post: PostVO) -> Result[SimplePost]:
        pass

    @abstractmethod
    def delete(self, post: PostVO) -> Result[PostId]:
        pass
