from typing import Optional
from dataclasses import dataclass

from Commons import Uid, Content, PostId


class Post:
    def __init__(
        self,
        title: str,
        content: Content,
        post_id: Optional[PostId] = None,
        user_id: Optional[Uid] = None,
    ):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.post_id = post_id


@dataclass(frozen=True)
class PostVO:
    title: str
    content: Content
    post_id: PostId
    user_id: Optional[Uid] = None
