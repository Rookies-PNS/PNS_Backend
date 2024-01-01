from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import secrets
from Domains.Entities import User, SimpleUser
from Commons import SessionData


@dataclass
class UserSession:
    session_key: str
    user: SimpleUser
    availability: SessionData

    def get_session_key(self) -> str:
        return self.session_key

    def get_user(self) -> SimpleUser:
        return self.user

    def get_publish_time(self) -> datetime:
        return self.availability.published_time.get_time()

    def get_is_delete(self) -> bool:
        return self.availability.is_disuse

    def check_avliable(self, session_minute: int) -> bool:
        """
        세션 사용 가능 여부를 확인하는 함수
        """
        return self.availability.check_avliable(session_minute)

    def republish_session(self, key: str):
        self.session_key = key
        return self.availability.republish_session()
