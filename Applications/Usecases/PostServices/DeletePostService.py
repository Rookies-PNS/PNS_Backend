import __init__
from typing import Optional, Dict

from Commons import *
from Domains.Entities import (
    SimpleUser,
    PostVO,
)
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IPostReadableRepository,
    IUserReadableRepository,
)

from Applications.Results import (
    Result,
    Fail,
)

from icecream import ic


class DeletePostService:
    def __init__(
        self,
        post_repoW: IPostWriteableRepository,
        post_repoR: IPostReadableRepository,
        user_repo: IUserReadableRepository,
    ):
        self.post_repoW = post_repoW
        self.post_repoR = post_repoR
        self.user_repo = user_repo
        # pid , user
        self.cache: Dict[int, PostVO] = {}

    def check_auth_coms(
        self, actor: SimpleUser, target: SimpleUser, share_flag: bool
    ) -> bool:
        require_policy: IntersectionPolicy = IntersectionPolicy(
            [
                Policy.PostReadAblePolicy,
                Policy.PostDeleteAblePolicy,
            ]
        )

        return require_policy.chcek_auth(
            actor_auth_Archives=actor.auth,
            actor_uid=actor.get_uid(),
            target_owner_id=target.get_uid(),
            taget_allow_flag=share_flag,
        )

    def check_auth(self, actor: SimpleUser, post_id: int) -> bool:
        match self._________get_post(post_id):
            case post if isinstance(post, PostVO):
                flag = post.share_flag
                target = post.owner
            case _:
                return False
        return self.check_auth_coms(actor, target, flag)

    def _________get_post(self, post_id: int) -> Optional[PostVO]:
        if post_id in self.cache:
            ret = self.cache[post_id]
            del self.cache[post_id]
            return ret

        match self.post_repoR.search_by_available_pid(PostId(post_id)):
            case post if isinstance(post, PostVO):
                self.cache[post_id] = post
                return post
            case fail:
                ic(fail)
                return None

    def delete(self, actor: SimpleUser, post_id: int) -> Optional[Fail]:
        """_summary_

        Returns:
            _type_: None(Success) , Fail(Fail)
        """
        match self._________get_post(post_id):
            case post if isinstance(post, PostVO):
                ret = post
            case _:
                return Fail(type="Fail_to_DeletePostService_Not_Found")
        if self.check_auth_coms(actor, ret.owner, ret.share_flag):
            return self.post_repoW.delete(ret)
        return Fail(type="Fail_to_GetPrivatePostService_No_Auth")
