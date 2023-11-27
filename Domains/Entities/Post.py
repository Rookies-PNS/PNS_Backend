from typing import Optional
from dataclasses import dataclass
from icecream import ic

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
    
    def get_account(self)->str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.user_id.account
            case _:
                return "익명"
    def get_content(self)->str:
        return self.content.content
                    
    def get_username(self)->str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.name
            case _:
                return "익명"



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
    def get_account(self)->str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.user_id.account
            case _:
                return "익명"
    def get_content(self)->str:
        return self.content.content

    def get_username(self)->str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.name
            case _:
                return "익명"

@dataclass(frozen=True)
class SimplePost:
    title: str
    post_id: PostId
    create_time: PostCreateTime
    update_time: PostUpdateTime
    user: Optional[SimpleUser] = None
    def get_account(self)->str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.user_id.account
            case _:
                return "익명"
    def get_content(self)->str:
        return self.content.content
    def get_username(self)->str:
        match self.user:
            case user if isinstance(user, SimpleUser):
                return user.name
            case _:
                return "익명"

def PostVO_to_Post(postvo)->Post:
    return Post(
        postvo.title,
        postvo.content,
        postvo.create_time,
        postvo.update_time,
        postvo.post_id,
        postvo.user
    )

def Post_to_PostVO(post:Post) -> Optional[PostVO]:
    if post.post_id is None:
        return None
    if post.create_time is None:
        return None
    if post.update_time is None:
        return None
    return PostVO(
        post.title,
        post.content,
        post.post_id,
        post.create_time,
        post.update_time,
        post.user
    )