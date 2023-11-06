import __init__
from typing import Optional
from collections.abc import Collection
from abc import *

from Commons import Uid, PostId
from Domains.Models import Post, PostVO
from Applications.Results import Result


class IPostRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def save(self, post: Post) -> Result[PostVO]:
        pass

    @abstractclassmethod
    def get_all(self) -> Collection[PostVO]:
        pass

    @abstractclassmethod
    def search_by_uid(self, uid: Uid) -> Collection[PostVO]:
        pass

    @abstractclassmethod
    def search_by_postid(self, post_id: PostId) -> Optional[PostVO]:
        pass

    @abstractclassmethod
    def update(self, post: PostVO) -> Result[PostVO]:
        pass

    @abstractmethod
    def delete(self, post: PostVO) -> Result[PostId]:
        pass
