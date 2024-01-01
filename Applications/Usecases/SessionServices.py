import __init__
import secrets
from typing import List, Optional
from Commons import SessionData
from Applications.Results import Result, Fail, Fail_CheckUser_IDNotFound
from datetime import datetime, timedelta
from Applications.Repositories.Interfaces import (
    ISessionRepository,
    IUserReadableRepository,
)
from Domains.Entities import SimpleUser, UserSession


class PublichSessionService:
    def __init__(
        self, repository: ISessionRepository, user_repo: IUserReadableRepository
    ):
        self.repository = repository
        self.user_repo = user_repo

    def publicsh_session(self, user: SimpleUser) -> Result[UserSession]:
        # check user
        if not self.user_repo.check_exist_userid(user.get_account()):
            return Fail_CheckUser_IDNotFound()

        # ID 당 세션 1개 유지
        self.repository.delete_session(user.get_uid())

        session_key = secrets.token_hex(32)
        due_to = datetime.now() + timedelta(minutes=60)
        is_delete = False
        session = UserSession(
            session_key=session_key, user=user, availability=SessionData(datetime.now())
        )
        return self.repository.save_session(session)


class TakeUserService:
    def __init__(self, repository: ISessionRepository):
        self.repository = repository

    def take_user(self, session_key: str) -> Optional[SimpleUser]:
        return self.repository.session_to_user(session_key)
