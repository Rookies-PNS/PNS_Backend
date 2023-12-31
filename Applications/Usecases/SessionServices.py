import __init__
import secrets
from typing import List, Optional
from Applications.Results import Result,Fail
from datetime import datetime,timedelta
from Applications.Repositories.Interfaces import IUserRepository,SessionRepository
from Domains.Entities import User, SimpleUser,Session


class CreateSession:
    def __init__(self, repository: SessionRepository, user_repo: IUserRepository):
        self.repository = repository
        self.user_repo = user_repo
    def create(self,user=SimpleUser)->Result[Session]:
        # ID 당 세션 1개 유지 
        if self.repository.verify_Session(user.user_id):
            self.repository.delete_Session(user)
          
        user_vo = self.user_repo.search_by_userid(user.user_id)
        # 사용자 존재여부
        if user_vo is None:
            return Fail(type=f"{type(user)}_does_not_exist")
        session_key = secrets.token_hex(32)
        due_to = datetime.now() + timedelta(minutes=60)
        is_delete = False
        session = Session(session_key=session_key,user=user,due_to=due_to,is_delete=is_delete)
        return self.repository.publish_Session(session)


class verifySession:
    def __init__(self,repository:SessionRepository):
        self.repository = repository

    def check_session(self, session_key: str) -> Result[SimpleUser]:
        
        if not self.repository.verify_Session(session_key):
            return Fail(type="Invalid_Session_Key")

        session_result = self.repository.load_session(session_key)

        match session_result:
            case Session(user=user,
                         due_to=due_to,
                         is_delete=is_delete)if due_to >= datetime.now() and not is_delete:
                return user
            case _:
                return Fail(type="Fail_Load_Session")