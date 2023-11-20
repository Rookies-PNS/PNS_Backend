import __init__
from typing import List, Optional
from collections.abc import Collection

from Commons import PostId, PostCreateTime, PostUpdateTime, Content
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
        self, page: int = 0, posts_per_page: Optional[int] = None
    ) -> Collection[SimplePost]:
        """_summary_
        생성 날짜 오름차순으로 post list를 반환해 주는 함수
        page를 입력하면 posts_per_page 만큼의 post list를 반환해 준다.

        Args:
            page (int): page는 0번부터 시작, 가진 것 이상의 번호를 출력시 빈 collection 반환. Defaults to 0.
            posts_per_page (Optional[int], optional): None으로 지정시 모른 요소를 반환한다. Defaults to None.

        Returns:
            Collection[SimplePost]: _description_
        """
        return self.repository.get_post_per_page_list(
            page=page, posts_per_page=posts_per_page
        )


class CreatePost:
    def __init__(self, repository: IPostRepository):
        self.repository = repository

    def create(
        self, title: str, content: str, user: Optional[SimpleUser] = None
    ) -> Result[SimplePost]:
        from Applications.Usecases.AppUsecaseExtention import (
            validate_user_input,
            convert_to_content,
        )

        match validate_user_input(title):
            case value if isinstance(value, Fail):
                return Fail(type="Fail_CreatePost_Nonvalidated_Title")

        converted_content = convert_to_content(content)

        post = Post(title=title, content=converted_content, user=user)
        return self.repository.save(post)


class GetPost:
    def __init__(self, repository: IPostRepository):
        self.repository = repository

    def get_post(self, post_id: PostId) -> Optional[PostVO]:
        return self.repository.search_by_uid(post_id)


class UpdatePost:
    def __init__(self, repository: IPostRepository):
        self.repository = repository

    def update(
        self, post: PostVO, user: SimpleUser, title: str, content: str
    ) -> Result[SimplePost]:
        pass
