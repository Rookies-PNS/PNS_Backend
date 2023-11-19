import __init__
from typing import List, Optional
from collections.abc import Collection

from Commons import PostId, PostCreateTime, PostUpdateTime
from Domains.Entities import SimpleUser, Post, PostVO, SimplePost
from Applications.Repositories.Interfaces import IPostRepository
from Applications.Repositories.Queries import SortOperation

from Applications.Results import (
    Result,
    Fail,
)


class GetPostList:
    def __init__(self, repository: IPostRepository):
        self.repository = repository

    def get_list_no_filter(
        self, page: int, posts_per_page: int, sort: SortOperation = SortOperation.des
    ) -> Collection[PostVO]:
        pass


class CreatePost:
    def __init__(self, repository: IPostRepository):
        self.repository = repository

    def create(
        self, title: str, content: str, user: Optional[SimpleUser] = None
    ) -> Result[SimplePost]:
        pass


class UpdatePost:
    def __init__(self, repository: IPostRepository):
        self.repository = repository

    def update(
        self, post: PostVO, user: SimpleUser, title: str, content: str
    ) -> Result[SimplePost]:
        pass
