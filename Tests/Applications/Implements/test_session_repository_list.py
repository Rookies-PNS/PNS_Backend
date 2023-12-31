import __init__
import secrets
from typing import Optional, List
from datetime import datetime,timedelta
from Commons import UserId, Uid
from Domains.Entities import User,SimpleUser,Session
from Applications.Usecases.SessionServices import CreateSession,verifySession
from Applications.Repositories.Interfaces import SessionRepository
from Applications.Results import (Result,Fail)

from datetime import datetime
from typing import Optional, List

class TestSessionRepository:
    def __init__(self, sessions: List[Session] = []):
        self.sessions = sessions

    def publish_Session(self, user: SimpleUser) -> Result[Session]:
        new_session = Session(
            session_key=secrets.token_hex(32),
            user=user,
            due_to=datetime.now()+timedelta(minutes=10),  
            is_delete=False
        )
        self.sessions.append(new_session)
        return new_session  

    def load_session(self, session_key: str) -> Optional[Session]:
        
        for session in self.sessions:
            if session.get_Session_key() == session_key and not session.get_is_delete():
                return session
        return None 

    def verify_Session(self, session_key: str) -> bool:
        for session in self.sessions:
            if session.get_Session_key() == session_key and not session.get_is_delete():
                return True
        return False

    def delete_Session(self, user: SimpleUser) -> Optional[Fail]:
        for session in self.sessions:
            if session.get_user().check_equal(user.get_uid()):
                session.is_delete = True
                return None
        return Fail("Session not found for the user")

