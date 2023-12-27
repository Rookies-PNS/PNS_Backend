from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import secrets
from Commons import UserId, Uid

@dataclass
class User:
    def __init__(
        self,
        user_id: UserId,
        uid: Optional[Uid] = None,
    ):
        self.user_id = user_id
        self.uid = uid

    def get_account(self) -> str:
        return self.user_id.account

    def check_equal(self, uid: Optional[Uid]) -> bool:
        if self.uid == None:
            return False
        match uid:      #match python 3.10이후 도입
            case id if isinstance(id, Uid):
                return uid == self.uid
            case _:
                ...
        return False

    def get_uid(self) -> Optional[Uid]:
        return self.uid

@dataclass
class Session_key:
   session_lifetime: timedelta = timedelta(minutes=1)
   def __init__(self):
       self.user_sessions = {}

   def create_session_key(self, user: User) -> str:
       session_key = secrets.token_urlsafe(16)  
       self.user_sessions[session_key] = {'user': user, 'timestamp': datetime.now()}
       return session_key

   def get_user_from_session(self, session_key: str) -> Optional[User]:
        session_info = self.user_sessions.get(session_key)
        if session_info and (datetime.now() - session_info['timestamp'] <= self.session_lifetime):
            return session_info['user']
        else:
            return None
   def remove_expired_sessions(self):
        now = datetime.now()
        expired_sessions = [key for key, info in self.user_sessions.items()
                            if (now - info['timestamp'] > self.session_lifetime)]

        for key in expired_sessions:
            del self.user_sessions[key]