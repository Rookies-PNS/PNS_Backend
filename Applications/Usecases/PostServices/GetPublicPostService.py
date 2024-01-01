import __init__
from typing import List, Optional
from collections.abc import Collection
from datetime import datetime

from Commons import *
from Domains.Entities import SimplePost, SimpleUser, PostVO
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IUserWriteableRepository,
)

from Applications.Results import (
    Result,
    Fail,
)
from icecream import ic


class GetPublicPostService:
    def __init__(self, repository: IPostWriteableRepository):
        self.repository = repository

    def check_auth(self, user: SimpleUser) -> bool:
        return True

    def get_post_from_post_id(self, post_id: int) -> Optional[PostVO]:
        return PostVO(
            title="First Post Title",
            content="Test View",
            owner=SimpleUser(
                user_account=UserId(account="a"),
                nickname="test",
                uid=Uid(idx=1),
                auth=AuthArchives(auths=[]),
                post_count=PostCounter(last_update_date=UpdateableTime(datetime.now())),
            ),
            target_time=SelectTime(datetime.now()),
            create_time=TimeVO(datetime.now()),
            update_time=UpdateableTime(datetime.now()),
            post_id=PostId(1),
            share_flag=True,
            img_key=ImageKey("image1.jpg"),
        )
        post_id = PostId(idx=post_id)
        return self.repository.search_by_pid(post_id)

    def get_list_no_filter(
        self, page: int = 0, posts_per_page: Optional[int] = None
    ) -> Collection[SimplePost]:
        """_summary_
        생성 날짜 오름차순으로 post list를 반환해 주는 함수
        page를 입력하면 posts_per_page 만큼의 post list를 반환해 준다.

        Args:
            page (int): page는 0번부터 시작, 가진 것 이상의 번호를 출력시 빈 collection 반환. Defaults to 0.
            posts_per_page (Optional[int], optional): None으로 지정시 모든 요소를 반환한다. Defaults to None.

        Returns:
            Collection[SimplePost]: _description_
        """
        return [
            SimplePost(
                title="test",
                post_id=PostId(1),
                owner=SimpleUser(
                    user_account=UserId(account="a"),
                    nickname="test",
                    uid=Uid(idx=1),
                    auth=AuthArchives(auths=[]),
                    post_count=PostCounter(
                        last_update_date=UpdateableTime(datetime.now())
                    ),
                ),
                target_time=SelectTime(datetime.now()),
            )
        ]

        return self.repository.get_post_per_page_list(
            page=page, posts_per_page=posts_per_page
        )
