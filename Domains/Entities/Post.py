from typing import Optional
from dataclasses import dataclass

from Commons import (
    Content,
    PostId,
    TimeVO,
    UpdateableTime,
    get_current_time,
    Uid,
)
from Domains.Entities.User import SimpleUser


class Post:
    def __init__(
        self,
        title: str,
        content: Content,
        user: SimpleUser,
        create_time: Optional[TimeVO] = None,
        update_time: Optional[UpdateableTime] = None,
        post_id: Optional[PostId] = None,
    ):
        self.title = title
        self.content = content
        self.user = user
        self.post_id = post_id
        match create_time:
            case time if isinstance(time, TimeVO):
                self.create_time = time
            case _:
                self.create_time = TimeVO(time=get_current_time())

        match update_time:
            case time if isinstance(time, UpdateableTime):
                self.update_time = time
            case _:
                self.update_time = UpdateableTime(time=get_current_time())

    def set_update_time(self):
        self.update_time.set_now()

    def get_account(self) -> str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.get_account()
            case _:
                return "익명"

    def get_content(self) -> str:
        return self.content.content

    def get_username(self) -> str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.get_user_nickname()
            case _:
                return "익명"

    def get_uid(self) -> Optional[Uid]:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.get_uid()
            case _:
                return None


@dataclass(frozen=True)
class SimplePost:
    title: str
    post_id: PostId
    user: SimpleUser
    create_time: TimeVO
    update_time: UpdateableTime

    def get_account(self) -> str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.get_account()
            case _:
                return "익명"

    def get_title(self) -> str:
        return self.title

    def get_uid(self) -> Optional[Uid]:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.get_uid()
            case _:
                return None

    def get_username(self) -> str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.get_user_nickname()
            case _:
                return "익명"


@dataclass(frozen=True)
class PostVO:
    title: str
    content: Content
    post_id: PostId
    user: SimpleUser
    create_time: TimeVO
    update_time: UpdateableTime

    def get_simple_post(self) -> SimplePost:
        return SimplePost(
            title=self.title,
            post_id=self.post_id,
            create_time=self.create_time,
            update_time=self.update_time,
            user=self.user,
        )

    def get_account(self) -> str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.get_account()
            case _:
                return "익명"

    def get_title(self) -> str:
        return self.title

    def get_content(self) -> str:
        return self.content.content

    def get_username(self) -> str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.get_user_nickname()
            case _:
                return "익명"

    def get_uid(self) -> Optional[Uid]:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.get_uid()
            case _:
                return None


def PostVO_to_Post(postvo: PostVO) -> Post:
    import copy

    return Post(
        title=postvo.title,
        content=postvo.content,
        create_time=postvo.create_time,
        update_time=copy.copy(postvo.update_time),
        post_id=postvo.post_id,
        user=postvo.user,
    )


def Post_to_PostVO(post: Post) -> Optional[PostVO]:
    if post.post_id is None:
        return None
    if post.create_time is None:
        return None
    if post.update_time is None:
        return None
    return PostVO(
        title=post.title,
        content=post.content,
        post_id=post.post_id,
        create_time=post.create_time,
        update_time=post.update_time,
        user=post.user,
    )
