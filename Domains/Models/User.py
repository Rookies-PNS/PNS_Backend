from typing import List, Optional

from Commons import UserID, Password, PostID


class User:
    def __init__(
        self,
        user_id: UserID,
        name: str,
        password: Password,
        posts: Optional[List[PostID]] = None,
    ):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.posts = posts
