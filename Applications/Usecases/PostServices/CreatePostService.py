import __init__
from typing import Optional
from datetime import datetime


from Commons import *
from Domains.Entities import (
    SimpleUser,
    Post,
    SimplePost,
)
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IUserWriteableRepository,
)

from Applications.Results import (
    Result,
    Fail,
)


class CreatePostService:
    def __init__(
        self, repository: IPostWriteableRepository, user_repo: IUserWriteableRepository
    ):
        self.repository = repository
        self.user_repo = user_repo

    def check_auth(self, actor: SimpleUser) -> bool:
        require_policy: IntersectionPolicy = IntersectionPolicy(
            [
                Policy.PostCreateAndUpdateAblePolicy,
                Policy.PostReadAblePolicy,
            ]
        )
        return require_policy.chcek_auth(
            actor_auth_Archives=actor.auth,
            actor_uid=actor.get_uid(),
            target_owner_id=actor.get_uid(),
        )

    def create(
        self,
        title: str,
        content: str,
        user: SimpleUser,
        share_flag: bool,
        target_time: datetime,
        img,
        create_time: Optional[datetime] = None,
    ) -> Result[SimplePost]:
        from Applications.Usecases.AppUsecaseExtention import (
            validate_user_input,
        )

        if not self.check_auth(user):
            return Fail("Fail_Have_Not_CreatePost_Auth")
        match user:
            case u if isinstance(u, SimpleUser):
                if not self.user_repo.check_exist_userid(u.get_account()):
                    return Fail(type="Fail_CreatePost_UserNotExist")
            case _:
                return Fail(type="Fail_CreatePost_NoUser")

        match validate_user_input(title, 250):
            case value if isinstance(value, Fail):
                return Fail(type="Fail_CreatePost_Nonvalidated_Title")
        if not validate_user_input(title, 250):
            return Fail(type="Fail_to_Much_Title_(250)")
        if not validate_user_input(content, 7000):
            return Fail(type="Fail_to_Much_Content_(7000)")

        match target_time:
            case time if isinstance(time, datetime):
                
        match create_time:
            case _ if isinstance(create_time, datetime):
                create_time = TimeVO(time=create_time)
                update_time = UpdateableTime(time=create_time.time)
            case _:
                create_time = TimeVO(time=datetime.now())
                update_time = UpdateableTime(time=create_time.time)

        post = Post(
            title=title,
            content=content,
            create_time=create_time,
            update_time=update_time,
            owner=user,
        )
        return self.repository.save_post(post)
