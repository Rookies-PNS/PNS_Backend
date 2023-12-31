import __init__
from typing import Optional, List
from datetime import datetime

from Commons import (
    UserId,
    Password,
    UpdateableTime,
    LoginData,
    PostCounter,
    Policy,
    TargetScope,
    Policy,
    AuthArchives,
    IntersectionPolicy,
)
from Domains.Entities import User, SimpleUser
from Applications.Usecases.AppUsecaseExtention import validate_user_input

from Applications.Usecases.UserServices.UsecaseUserExtention import (
    check_valid_password,
    convert_to_Password_with_hashing,
    get_padding_adder,
    account_len,
    name_len,
    nickname_len,
)
from Applications.Repositories.Interfaces import (
    IUserWriteableRepository,
    IPostReadableRepository,
    IPostWriteableRepository,
)
from Applications.Results import (
    Result,
    Fail,
    Fail_CreateUser_IDAlreadyExists,
)


class DeleteUserService:
    def __init__(
        self,
        user_repository: IUserWriteableRepository,
        post_read_repository: IPostReadableRepository,
        post_write_repository: IPostWriteableRepository,
    ):
        self.user_repo = user_repository
        self.post_reader = post_read_repository
        self.post_writer = post_write_repository

    def check_auth(
        self,
        target: SimpleUser,
        actor: SimpleUser,
    ) -> bool:
        require_policy: IntersectionPolicy = IntersectionPolicy(
            [
                Policy.PostDeleteAblePolicy,
                Policy.UserDataDeleteAblePolicy,
            ]
        )
        return require_policy.chcek_auth(
            actor_auth_Archives=actor.auth,
            actor_uid=actor.get_uid(),
            target_owner_id=target.get_uid(),
        )

    def delete_user(
        self,
        target: SimpleUser,
        actor: SimpleUser,
        actor_passwd: str,
    ):
        pass
    
