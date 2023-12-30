import __init__
from typing import Optional
from collections.abc import Collection
from datetime import datetime

from Commons import Uid, UserId, PostId, TimeVO, UpdateableTime, Content
from Domains.Entities import PostVO, Post, SimplePost, SimpleUser
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IUserWriteableRepository,
)
from Applications.Results import Result, Fail

from icecream import ic
import pymysql


class MySqlPostReadStorage(IPostWriteableRepository):
    def __init__(self, user_repo: IUserWriteableRepository, name_padding: str = "log_"):
        self.name_padding = name_padding
        self.user_repo = user_repo

    def connect(self):
        from get_db_data import get_mysql_dict

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
                    content=Content(content=row["content"]),
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
                    content=Content(content=row["content"]),
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

    def save_post(self, post: Post) -> Result[SimplePost]:
        connection = self.connect()
        table_name = self.get_padding_name("post")
        try:
            with connection.cursor() as cursor:
                match post.user:
                    case user if isinstance(user, SimpleUser):
                        insert_query = f"INSERT INTO {table_name} (title, content, user_id, create_time, update_time) VALUES (%s, %s, %s, %s, %s);"
                        cursor.execute(
                            insert_query,
                            (
                                post.title,
                                post.content.content,
                                post.user.uid.idx,
                                post.create_time.get_time(),
                                post.update_time.get_time(),
                            ),
                        )
                    case none if none is None:
                        insert_query = f"INSERT INTO {table_name} (title, content, create_time, update_time) VALUES (%s, %s, %s, %s);"
                        cursor.execute(
                            insert_query,
                            (
                                post.title,
                                post.content.content,
                                post.create_time.get_time(),
                                post.update_time.get_time(),
                            ),
                        )
                    case d if isinstance(d, dict):
                        return Fail(
                            type="Fail_Mysql_SavePost_ValueError(user.type==dict)"
                        )
                    case _:
                        return Fail(type="Fail_Mysql_SavePost_unknown")
                # 마지막 실행 파일 찾기
                sql_query = f"SELECT * FROM {table_name} ORDER BY post_id DESC LIMIT 1;"
                cursor.execute(sql_query)

                # 결과 가져오기
                result = cursor.fetchone()

                if result:
                    ret = self._convert_to_postvo(result)
                else:
                    return Fail(type="Fail_Mysql_SavePost_GetFailID")
            connection.commit()
        except Exception as ex:
            connection.rollback()
            return Fail(type="Fail_Mysql_SavePost")
        finally:
            connection.close()

        match ret:
            case _ if isinstance(ret, PostVO):
                return ret.get_simple_post()
            case _:
                return Fail(type="Fail_Mysql_SavePost_NotSavedPost")

    def _get_post_per_page_list_all(self) -> Result[Collection[SimplePost]]:
        connection = self.connect()
        table_name = self.get_padding_name("post")

        # This query will return a list of post_ids in descending order, limited by posts_per_page and offset by page*posts_per_page
        select_query = f"SELECT * FROM {table_name} ORDER BY post_id DESC;"
        try:
            with connection.cursor() as cursor:
                # Execute the query with the given parameters
                cursor.execute(select_query)
                # Fetch all the results of the query
                results = cursor.fetchall()
        except Exception as ex:
            connection.rollback()
            return Fail(type="Fail_Mysql_LoadPostList_unknown")
        finally:
            connection.close()

        return [self._convert_to_postvo(row).get_simple_post() for row in results]

    def get_post_per_page_list(
        self,
        page: int = 0,
        posts_per_page: Optional[int] = None,
    ) -> Result[Collection[SimplePost]]:
        match posts_per_page:
            case _ if posts_per_page is not None:
                pass  # 아래에서 처리
            case _ if posts_per_page is None:
                return self._get_post_per_page_list_all()
            case _ if posts_per_page < 1:
                raise ValueError(
                    f"Must posts_per_page >= 1, current value({posts_per_page})"
                )

        connection = self.connect()
        table_name = self.get_padding_name("post")

        # This query will return a list of post_ids in descending order, limited by posts_per_page and offset by page*posts_per_page
        select_query = (
            f"SELECT * FROM {table_name} ORDER BY post_id DESC LIMIT %s OFFSET %s;"
        )
        try:
            with connection.cursor() as cursor:
                # Execute the query with the given parameters
                cursor.execute(select_query, (posts_per_page, (page) * posts_per_page))
                # Fetch all the results of the query
                results = cursor.fetchall()
        except Exception as ex:
            connection.rollback()
            return Fail(type="Fail_Mysql_LoadPostList_unknown")
        finally:
            connection.close()

        return [self._convert_to_postvo(row).get_simple_post() for row in results]

    def search_by_pid(self, post_id: PostId) -> Optional[PostVO]:
        connection = self.connect()
        table_name = self.get_padding_name("post")
        try:
            with connection.cursor() as cursor:
                select_query = f"SELECT * FROM {table_name} WHERE post_id = %s;"
                cursor.execute(select_query, (post_id.idx,))
                result = cursor.fetchone()

                if result:
                    return self._convert_to_postvo(result)
        except Exception as ex:
            connection.rollback()
        finally:
            connection.close()

    def search_by_uid(
        self,
        user_id: Uid,
        page: int = 0,
        posts_per_page: Optional[int] = None,
    ) -> Result[Collection[SimplePost]]:
        connection = self.connect()
        table_name = self.get_padding_name("post")

        select_query = f"SELECT * FROM {table_name} WHERE user_id = %s ORDER BY post_id DESC LIMIT %s OFFSET %s;"
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    select_query, (user_id.idx, posts_per_page, (page) * posts_per_page)
                )
                results = cursor.fetchall()
        except:
            connection.rollback()
            return Fail(type="Fail_Mysql_LoadPostList_unknown")
        finally:
            connection.close()

        return [self._convert_to_postvo(row).get_simple_post() for row in results]

    def update(self, post: PostVO) -> Result[SimplePost]:
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

        return self.search_by_pid(post.post_id).get_simple_post()

    def delete(self, post: PostVO) -> Result[PostId]:
        connection = self.connect()
        table_name = self.get_padding_name("post")

        delete_query = f"DELETE FROM {table_name} WHERE post_id = %s;"
        try:
            with connection.cursor() as cursor:
                cursor.execute(delete_query, (post.post_id.idx,))
                connection.commit()
        except:
            connection.rollback()
            return Fail(type="Fail_Mysql_DeletePost_unknown")
        finally:
            connection.close()

        return post.post_id
