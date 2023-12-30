import __init__
from typing import Optional
from datetime import datetime


from Commons import TimeVO, UpdateableTime
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

    def check_auth(self, user: SimpleUser) -> bool:
        match user:
            case u if isinstance(u, SimpleUser):
                if self.user_repo.check_exist_userid(u.get_account()):
                    return True
        return False

    def create(
        self,
        title: str,
        content: str,
        user: SimpleUser,
        create_time: Optional[datetime] = None,
    ) -> Result[SimplePost]:
        from Applications.Usecases.AppUsecaseExtention import (
            validate_user_input,
            convert_to_content,
        )

        match create_time:
            case _ if isinstance(create_time, datetime):
                create_time = TimeVO(time=create_time)
                update_time = UpdateableTime(time=create_time.time)
            case _:
                create_time = TimeVO(time=datetime.now())
                update_time = UpdateableTime(time=create_time.time)

        match user:
            case u if isinstance(u, SimpleUser):
                if not self.user_repo.check_exist_userid(u.get_account()):
                    return Fail(type="Fail_CreatePost_UserNotExist")
            case _:
                return Fail(type="Fail_CreatePost_NoUser")

        match validate_user_input(title, 250):
            case value if isinstance(value, Fail):
                return Fail(type="Fail_CreatePost_Nonvalidated_Title")

        converted_content = convert_to_content(content)

        post = Post(
            title=title,
            content=converted_content,
            create_time=create_time,
            update_time=update_time,
            user=user,
        )
        return self.repository.save_post(post)
