import __init__
from typing import Optional

from Commons import PostId
from Domains.Entities import (
    SimpleUser,
    PostVO,
)
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IUserWriteableRepository,
)

from Applications.Results import (
    Result,
    Fail,
)


class DeletePostService:
    def __init__(
        self, post_repo: IPostWriteableRepository, user_repo: IUserWriteableRepository
    ):
        self.post_repo = post_repo
        self.user_repo = user_repo

    def check_auth(self, post: PostVO, user: SimpleUser) -> bool:
        return True
        if not self.post_repo.check_exist_pid(post.post_id):
            return False

        match post.user:
            case user_in_post if isinstance(user_in_post, SimpleUser):
                # Check if user_in_post and user are the same
                if user_in_post == user:
                    return True
        return False

    def delete(self, post: PostVO, user: Optional[SimpleUser] = None) -> Result[PostId]:
        if not self.post_repo.check_exist_pid(post.post_id):
            return Fail(type="Fail_Post_NotExist")
        match post.user:
            case user_in_post if isinstance(user_in_post, SimpleUser):
                # Check if user_in_post and user are the same
                if user_in_post == user:
                    pass
                else:
                    return Fail(type="Fail_DeletePost_UserMismatch")
            case None:
                # Anonymous posts can be deleted by anyone
                return Fail(type="Fail_DeletePost_NoUser")
        return self.post_repo.delete(post)
