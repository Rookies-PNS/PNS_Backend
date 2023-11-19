from typing import Optional
from dataclasses import dataclass

from Commons import Content, PostId, PostCreateTime, PostUpdateTime, get_current_time
from Domains.Entities.User import SimpleUser


class Post:
    def __init__(
        self,
        title: str,
        content: Content,
        create_time: Optional[PostCreateTime] = None,
        update_time: Optional[PostUpdateTime] = None,
        post_id: Optional[PostId] = None,
        user: Optional[SimpleUser] = None,
    ):
        self.title = title
        self.content = content
        self.user = user
        self.post_id = post_id
        match create_time:
            case _ if create_time is not None:
                self.create_time = create_time
            case _:
                self.create_time = PostCreateTime(time=get_current_time())
        match update_time:
            case _ if update_time is not None:
                self.update_time = update_time
            case _:
                self.update_time = PostUpdateTime(time=get_current_time())

    def set_update_time(self):
        self.update_time.set_time()


@dataclass(frozen=True)
class PostVO:
    title: str
    content: Content
    post_id: PostId
    create_time: PostCreateTime
    update_time: PostUpdateTime
    user: Optional[SimpleUser] = None

    def get_simple_post(self):
        return SimplePost(
            title=self.title,
            post_id=self.post_id,
            create_time=self.create_time,
            update_time=self.update_time,
            user=self.user,
        )


@dataclass(frozen=True)
class SimplePost:
    title: str
    post_id: PostId
    create_time: PostCreateTime
    update_time: PostUpdateTime
    user: Optional[SimpleUser] = None
