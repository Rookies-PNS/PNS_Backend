from typing import Optional
from dataclasses import dataclass

from Commons import (
    Content,
    PostId,
    TimeVO,
    UpdateableTime,
    SelectTime,
    get_current_time,
    Uid,
    ImageKey,
)
from Domains.Entities.User import SimpleUser


class CommonPostAction:
    title: str
    post_id: PostId
    owner: SimpleUser
    target_time: SelectTime
    share_flag: bool = False
    img_key: Optional[ImageKey] = None

    def get_account(self) -> str:
        match self.owner:
            case user if isinstance(user, SimpleUser):
                return user.get_account()
            case _:
                return "익명"

    def get_title(self) -> str:
        return self.title

    def get_post_id(self) -> PostId:
        return self.post_id

    def get_uid(self) -> Uid:
        match self.owner:
            case user if isinstance(user, SimpleUser):
                return user.get_uid()
            case _:
                raise ValueError()

    def get_owner_nickname(self) -> str:
        match self.owner:
            case user if isinstance(user, SimpleUser):
                return user.get_user_nickname()
            case _:
                return "익명"


@dataclass(frozen=True)
class SimplePost(CommonPostAction):
    title: str
    post_id: PostId
    owner: SimpleUser
    target_time: SelectTime
    share_flag: bool = False
    img_key: Optional[ImageKey] = None

    def get_uid(self) -> Uid:
        match self.owner:
            case user if isinstance(user, SimpleUser):
                return user.get_uid()
            case _:
                raise ValueError(
                    f"SimplePost.get_uid - {self.owner}({type(self.owner)})"
                )


class FullPostAction(CommonPostAction):
    title: str
    post_id: PostId
    owner: SimpleUser
    target_time: SelectTime
    content: str
    create_time: TimeVO
    update_time: UpdateableTime
    share_flag: bool = False
    img_key: Optional[ImageKey] = None

    def set_update_time(self):
        self.update_time.set_now()

    def get_content(self) -> str:
        return self.content.content


@dataclass
class Post(FullPostAction):
    title: str
    content: str
    owner: SimpleUser
    target_time: SelectTime
    create_time: TimeVO
    update_time: UpdateableTime
    post_id: Optional[PostId] = None
    share_flag: bool = False
    img_key: Optional[ImageKey] = None

    def get_post_id(self) -> Optional[PostId]:
        return self.post_id


@dataclass(frozen=True)
class PostVO(FullPostAction):
    title: str
    content: str
    owner: SimpleUser
    target_time: SelectTime
    create_time: TimeVO
    update_time: UpdateableTime
    post_id: PostId
    share_flag: bool = False
    img_key: Optional[ImageKey] = None

    def get_simple_post(self) -> SimplePost:
        return SimplePost(
            title=self.title,
            post_id=self.post_id,
            owner=self.owner,
            target_time=self.target_time,
            share_flag=self.share_flag,
            img_key=self.img_key,
        )


def PostVO_to_Post(postvo: PostVO) -> Post:
    import copy

    return Post(
        title=postvo.title,
        content=postvo.content,
        owner=postvo.owner,
        target_time=postvo.target_time,
        share_flag=postvo.share_flag,
        img_key=postvo.img_key,
        create_time=postvo.create_time,
        update_time=copy.copy(postvo.update_time),
        post_id=postvo.post_id,
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
        owner=post.owner,
        target_time=post.target_time,
        share_flag=post.share_flag,
        img_key=post.img_key,
        create_time=post.create_time,
        update_time=UpdateableTime(post.update_time.get_time()),
        post_id=post.post_id,
    )
