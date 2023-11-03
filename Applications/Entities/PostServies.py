from typing import Optional
from dataclasses import dataclass

from Commons import Uid, Content, PostId
from Domains.Models import Post


@dataclass(frozen=True)
class PostVO:
    title: str
    content: Content
    post_id: PostId
    user_id: Optional[Uid] = None
