import __init__
from typing import List, Optional, Dict
from collections.abc import Collection
from datetime import datetime, timedelta
from Commons import *
from Domains.Entities import (
    SimplePost,
    SimpleUser,
    PostVO,
    Post_to_PostVO,
    PostVO_to_Post,
)
from Applications.Repositories.Interfaces import (
    IUserWriteableRepository,
    IPostReadableRepository,
)

from Applications.Results import (
    Result,
    Fail,
)
from icecream import ic


class GetPrivatePostService:
    def __init__(self, repository: IPostReadableRepository):
        self.repository = repository

        # pid , user
        self.cache: Dict[int, PostVO] = {}

    def _______chece_auth(
        self, actor: SimpleUser, target: SimpleUser, share_flag: bool
    ) -> bool:
        require_policy: IntersectionPolicy = IntersectionPolicy(
            [Policy.PostReadAblePolicy]
        )

        return require_policy.chcek_auth(
            actor_auth_Archives=actor.auth,
            actor_uid=actor.get_uid(),
            target_owner_id=target.get_uid(),
            taget_allow_flag=share_flag,
        )

    def get_post_list(
        self, actor: SimpleUser, page: int = 0, posts_per_page: Optional[int] = None
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

        match self.repository.search_by_available_uid(
            user_id=actor.get_uid(), page=page, posts_per_page=posts_per_page
        ):
            case ret if isinstance(ret, list):
                return ret
            case fail if isinstance(fail, Fail):
                ic(fail)
                return []
            case _:
                return []

    def chece_auth(self, actor: SimpleUser, post_id: int) -> bool:
        match self._________get_simple_post(post_id):
            case post if isinstance(post, PostVO):
                flag = post.share_flag
                target = post.owner
            case _:
                return False
        return self._______chece_auth(actor, target, flag)

    def _________get_simple_post(self, post_id: int) -> Optional[PostVO]:
        if post_id in self.cache:
            ret = self.cache[post_id]
            del self.cache[post_id]
            return ret

        match self.repository.search_by_pid(PostId(post_id)):
            case post if isinstance(post, PostVO):
                self.cache[post_id] = post
                return post
            case fail:
                ic(fail)
                return None

    def get_post_detail(self, actor: SimpleUser, post_id: int) -> Result[PostVO]:
        match self._________get_simple_post(post_id):
            case post if isinstance(post, PostVO):
                ret = post
            case _:
                return Fail(type="Fail_to_GetPrivatePostService_Not_Found")
        if self._______chece_auth(actor, ret.owner, ret.share_flag):
            return ret
        return Fail(type="Fail_to_GetPrivatePostService_No_Auth")
