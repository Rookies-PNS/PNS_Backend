from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import secrets
from Domains.Entities import User,SimpleUser
from Commons import get_current_time
# @dataclass
# class Session_key:
#    session_lifetime: timedelta = timedelta(minutes=1)
#    def __init__(self):
#        self.user_sessions = {}

#    def create_session_key(self, user: User) -> str:
#        session_key = secrets.token_urlsafe(16)  
#        self.user_sessions[session_key] = {'user': user, 'timestamp': datetime.now()}
#        return session_key

#    def get_user_from_session(self, session_key: str) -> Optional[User]:
#         session_info = self.user_sessions.get(session_key)
#         if session_info and (datetime.now() - session_info['timestamp'] <= self.session_lifetime):
#             return session_info['user']
#         else:
#             return None
#    def remove_expired_sessions(self):
#         now = datetime.now()
#         expired_sessions = [key for key, info in self.user_sessions.items()
#                             if (now - info['timestamp'] > self.session_lifetime)]

#         for key in expired_sessions:
#             del self.user_sessions[key]

@dataclass
class Session:
    session_key:str
    user:SimpleUser
    due_to:datetime
    is_delete:bool

    def get_Session_key(self) -> str:
        return self.session_key
    
    def get_user(self) -> SimpleUser:
        return self.user
    
    def get_due_to(self) -> datetime:
        return self.due_to
    
    def get_is_delete(self) -> bool:
        return self.is_delete
    
