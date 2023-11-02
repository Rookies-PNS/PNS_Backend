from typing import List, Optional

from Commons import UserID, Password


class User:
    def __init__(self, user_id: UserID, name: str, password: Password):
        self.user_id = user_id
        self.name = name
        self.password = password
