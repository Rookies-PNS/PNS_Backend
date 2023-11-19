import __init__
from typing import Optional
from collections.abc import Collection

from Commons import Uid, UserId, PostId
from Domains.Entities import PostVO, Post
from Applications.Repositories.Interfaces import IPostRepository
from Applications.Results import Result, Fail

import pymysql


class MySqlPostStorage(IPostRepository):
    def __init__(self, name_padding: str = "log_"):
        self.name_padding = name_padding

    def connect(self):
        from get_db_data import get_mysql_dict

        sql_config = get_mysql_dict()
        return pymysql.connect(
            host=sql_config["host"],
            user=sql_config["user"],
            password=sql_config["password"],
            db=sql_config["database"],
            charset=sql_config["charset"],
        )

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"

    def save(self, post: Post) -> Result[PostVO]:
        pass

    def get_list(self) -> Collection[PostVO]:
        pass

    def search_by_uid(self, uid: Uid) -> Collection[PostVO]:
        pass

    def search_by_postid(self, post_id: PostId) -> Optional[PostVO]:
        pass

    def update(self, post: PostVO) -> Result[PostVO]:
        pass

    def delete(self, post: PostVO) -> Result[PostId]:
        pass
