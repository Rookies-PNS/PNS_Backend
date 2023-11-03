from typing import List, Optional
from dataclasses import dataclass

from Commons import UserIdVO, Password, PostId


@dataclass(frozen=True)
class UserVO:
    user_id: UserIdVO
    name: str
    password: Password
    posts: Optional[List[PostId]] = None
