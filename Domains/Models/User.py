from typing import List, Optional

from Commons import UserId, Password, PostId


class User:
    def __init__(
        self,
        user_id: UserId,
        name: str,
        password: Password,
        posts: Optional[List[PostId]] = None,
    ):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.posts = posts
