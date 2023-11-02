from typing import List, Optional

from Commons import UserID, Content, PostID


class Post:
    def __init__(
        self,
        title: str,
        content: Content,
        user_id: Optional[UserID] = None,
        post_id: Optional[PostID] = None,
    ):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.post_id = post_id
