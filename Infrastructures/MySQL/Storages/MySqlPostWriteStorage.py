import __init__
from typing import Optional
from collections.abc import Collection
from datetime import datetime

from Commons import *
from Domains.Entities import PostVO, Post, SimplePost, SimpleUser, ImageData
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IUserWriteableRepository,
)
from Applications.Results import Result, Fail

from icecream import ic
import pymysql


class MySqlPostWriteStorage(IPostWriteableRepository):
    def __init__(self, user_repo: IUserWriteableRepository, name_padding: str = "log_"):
        self.name_padding = name_padding
        self.user_repo = user_repo

    def connect(self):
        from get_config_data import get_mysql_dict

        sql_config = get_mysql_dict()
        return pymysql.connect(
            host=sql_config["host"],
            user=sql_config["user"],
            password=sql_config["password"],
            db=sql_config["database"],
            charset=sql_config["charset"],
            cursorclass=pymysql.cursors.DictCursor,
        )

    def _convert_to_postvo(self, row: dict) -> PostVO:
        match row["user_id"]:
            case user_id if user_id is not None:
                return PostVO(
                    title=row["title"],
                    content=row["content"],
                    create_time=TimeVO(
                        time=row["create_time"]
                    ),  # time=datetime.strptime(row["create_time"], '%Y-%m-%d %H:%M:%S')),
                    update_time=UpdateableTime(
                        time=row["update_time"]
                    ),  # time=datetime.strptime(row["update_time"], '%Y-%m-%d %H:%M:%S')),
                    post_id=PostId(idx=row["post_id"]),
                    user=self.user_repo.search_by_uid(
                        Uid(idx=row["user_id"])
                    ).get_simple_user(),
                )
            case _:
                return PostVO(
                    title=row["title"],
                    content=row["content"],
                    create_time=TimeVO(
                        time=row["create_time"]
                    ),  # time=datetime.strptime(row["create_time"], '%Y-%m-%d %H:%M:%S')),
                    update_time=UpdateableTime(
                        time=row["update_time"]
                    ),  # time=datetime.strptime(row["update_time"], '%Y-%m-%d %H:%M:%S')),
                    post_id=PostId(idx=row["post_id"]),
                    user=None,
                )

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"

    def check_exist_pid(self, post_id: PostId) -> bool:
        connection = self.connect()
        table_name = self.get_padding_name("post")
        select_query = f"SELECT post_id FROM {table_name} WHERE post_id = %s;"
        try:
            with connection.cursor() as cursor:
                cursor.execute(select_query, (post_id.idx,))
                result = cursor.fetchone()
        except:
            connection.rollback()
            return False
        finally:
            connection.close()

        return result is not None

    def save_post(self, post: Post) -> Optional[Fail]:
        connection = self.connect()
        table_name = self.get_padding_name("post")
        insert_query = f"""
INSERT INTO {table_name}
(
    title,
    content,
    target_time,
    create_time,
    update_time,
    share_flag,"""
        try:
            with connection.cursor() as cursor:
                match post.get_img_key():
                    case key if isinstance(key, str):
                        insert_query += """
    img_access_key,
    owner_id
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""
                    case _:
                        insert_query += """                       
    owner_id
)
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""
                match post.get_img_key():
                    case key if isinstance(key, str):
                        cursor.execute(
                            insert_query,
                            (
                                post.get_title(),
                                post.get_content(),
                                post.target_time.get_time(),
                                post.create_time.get_time(),
                                post.update_time.get_time(),
                                post.share_flag,
                                post.get_img_key(),
                                post.get_uid().idx,
                            ),
                        )

                    case _:
                        cursor.execute(
                            insert_query,
                            (
                                post.get_title(),
                                post.get_content(),
                                post.target_time.get_time(),
                                post.create_time.get_time(),
                                post.update_time.get_time(),
                                post.share_flag,
                                post.get_uid().idx,
                            ),
                        )

                connection.commit()
        except:  # Exception as ex:
            connection.rollback()
            return Fail(type="Fail_Mysql_SavePost")
        finally:
            connection.close()

    def update_all(self, post: PostVO) -> Result[PostId]:
        connection = self.connect()
        table_name = self.get_padding_name("post")

        update_query = f"UPDATE {table_name} SET title = %s, content = %s, update_time = %s WHERE post_id = %s;"
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    update_query,
                    (
                        post.title,
                        post.content.content,
                        post.update_time.get_time(),
                        post.post_id.idx,
                    ),
                )
                connection.commit()
        except Exception as ex:
            connection.rollback()
            return Fail(type="Fail_Mysql_UpdatePost_unknown")
        finally:
            connection.close()

        return post.get_post_id()

    def update_share(self, post: SimplePost) -> Result[PostId]:
        """_summary_
        일기의 공유설정을 변경한다.

        Args:
            post (SimplePost): _description_

        Returns:
            Result[PostId]: _description_
        """
        return NotImplementedError()

    def update_image_data(self, image_data: ImageData) -> Optional[Fail]:
        return NotImplementedError()

    def delete(self, post: PostVO) -> Optional[Fail]:
        connection = self.connect()
        table_name = self.get_padding_name("post")

        delete_query = f"""
UPDATE {table_name}
SET delete_flag = True
WHERE post_id = %s;
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(delete_query, (post.get_post_id().idx,))
                connection.commit()

        except Exception as ex:
            connection.rollback()
            return Fail(type="Fail_Mysql_DeletePost_unknown")
        finally:
            connection.close()
