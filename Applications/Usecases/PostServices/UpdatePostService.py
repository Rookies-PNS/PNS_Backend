import __init__
from typing import List, Optional
from collections.abc import Collection
from datetime import datetime

from Commons import PostId, TimeVO, UpdateableTime
from Domains.Entities import (
    SimpleUser,
    Post,
    PostVO,
    SimplePost,
    Post_to_PostVO,
    PostVO_to_Post,
)
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IUserWriteableRepository,
)

from Applications.Results import (
    Result,
    Fail,
)


class UpdatePostService:
    def __init__(
        self, post_repo: IPostWriteableRepository, user_repo: IUserWriteableRepository
    ):
        self.post_repo = post_repo
        self.user_repo = user_repo

    def check_auth(self, post: PostVO, user: SimpleUser) -> bool:
        if not self.post_repo.check_exist_pid(post.post_id):
            return False

        match post.user:
            case user_in_post if isinstance(user_in_post, SimpleUser):
                # Check if user_in_post and user are the same
                if user_in_post == user:
                    return True
        return False

    def update(
        self, post: PostVO, title: str, content: str, user: SimpleUser
    ) -> Result[SimplePost]:
        from Applications.Usecases.AppUsecaseExtention import (
            validate_user_input,
            convert_to_content,
        )

        if not self.post_repo.check_exist_pid(post.post_id):
            return Fail(type="Fail_Post_NotExist")

        match post.user:
            case user_in_post if isinstance(user_in_post, SimpleUser):
                # Check if user_in_post and user are the same
                if user_in_post == user:
                    pass
                else:
                    return Fail(type="Fail_UpdatePost_UserMismatch")
            case none if none is None:
                # Anonymous posts can be deleted by anyone
                return Fail(type="Fail_UpdatePost_NoUser")

        match validate_user_input(title, 250):
            case value if isinstance(value, Fail):
                return Fail(type="Fail_UpdatePost_Nonvalidated_Title")

        converted_content = convert_to_content(content)
        convert_post = PostVO_to_Post(post)
        convert_post.title = title
        convert_post.set_update_time()

        match converted_content:
            case fail if isinstance(fail, Fail):
                return fail
            case new_content if isinstance(new_content, Content):
                # update
                convert_post.content = new_content
                updated_post = Post_to_PostVO(convert_post)
                if updated_post is not None:
                    return self.post_repo.update(updated_post)
                else:
                    return Fail(type=f"Fail_UpdatePost_ConvertFail")
            case _:
                return Fail(type=f"Fail_UpdatePost_Unknown_type")
