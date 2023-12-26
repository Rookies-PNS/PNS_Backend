import __init__
from typing import List, Optional
from collections.abc import Collection
from datetime import datetime

from Commons import PostId, PostCreateTime, PostUpdateTime, Content
from Domains.Entities import (
    SimpleUser,
    Post,
    PostVO,
    SimplePost,
    Post_to_PostVO,
    PostVO_to_Post,
)
from Applications.Repositories.Interfaces import IPostRepository, IUserRepository
from Applications.Repositories.Queries import SortOperation

from Applications.Results import (
    Result,
    Fail,
)
from icecream import ic


class GetPostList:
    def __init__(self, repository: IPostRepository):
        self.repository = repository

    def get_list_no_filter(
        self, page: int = 0, posts_per_page: Optional[int] = None
    ) -> Collection[SimplePost]:
        """_summary_
        생성 날짜 오름차순으로 post list를 반환해 주는 함수
        page를 입력하면 posts_per_page 만큼의 post list를 반환해 준다.

        Args:
            page (int): page는 0번부터 시작, 가진 것 이상의 번호를 출력시 빈 collection 반환. Defaults to 0.
            posts_per_page (Optional[int], optional): None으로 지정시 모든 요소를 반환한다. Defaults to None.

        Returns:
            Collection[SimplePost]: _description_
        """
        return self.repository.get_post_per_page_list(
            page=page, posts_per_page=posts_per_page
        )


class CreatePost:
    def __init__(self, repository: IPostRepository, user_repo: IUserRepository):
        self.repository = repository
        self.user_repo = user_repo

    def check_auth(self, user: SimpleUser) -> bool:
        match user:
            case u if isinstance(u, SimpleUser):
                if self.user_repo.check_exist_userid(u.get_account()):
                    return True
        return False

    def create(
        self,
        title: str,
        content: str,
        user: SimpleUser,
        create_time: Optional[datetime] = None,
    ) -> Result[SimplePost]:
        from Applications.Usecases.AppUsecaseExtention import (
            validate_user_input,
            convert_to_content,
        )

        match create_time:
            case _ if isinstance(create_time, datetime):
                create_time = PostCreateTime(time=create_time)
                update_time = PostUpdateTime(time=create_time.time)
            case _:
                create_time = PostCreateTime(time=datetime.now())
                update_time = PostUpdateTime(time=create_time.time)

        match user:
            case u if isinstance(u, SimpleUser):
                if not self.user_repo.check_exist_userid(u.get_account()):
                    return Fail(type="Fail_CreatePost_UserNotExist")
            case _:
                return Fail(type="Fail_CreatePost_NoUser")

        match validate_user_input(title, 250):
            case value if isinstance(value, Fail):
                return Fail(type="Fail_CreatePost_Nonvalidated_Title")

        converted_content = convert_to_content(content)

        post = Post(
            title=title,
            content=converted_content,
            create_time=create_time,
            update_time=update_time,
            user=user,
        )
        return self.repository.save(post)


class GetPost:
    def __init__(self, repository: IPostRepository):
        self.repository = repository

    def check_auth(self, user: SimpleUser) -> bool:
        return True

    def get_post_from_post_id(self, post_id: int) -> Optional[PostVO]:
        post_id = PostId(idx=post_id)
        return self.repository.search_by_pid(post_id)


class DeletePost:
    def __init__(self, post_repo: IPostRepository, user_repo: IUserRepository):
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


class UpdatePost:
    def __init__(self, post_repo: IPostRepository, user_repo: IUserRepository):
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
