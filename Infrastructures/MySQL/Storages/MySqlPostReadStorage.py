import __init__
from typing import Optional, List, Dict
from collections.abc import Collection
from datetime import datetime


from Commons import *
from Domains.Entities import PostVO, Post, SimplePost, SimpleUser, UserVO
from Applications.Repositories.Interfaces import (
    IPostReadableRepository,
    IUserReadableRepository,
)
from Applications.Results import Result, Fail

from icecream import ic
import pymysql


class MySqlPostReadStorage(IPostReadableRepository):
    def __init__(self, user_repo: IUserReadableRepository, name_padding: str = "log_"):
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
        a = PostVO(
            title=row["title"],
            content=row["content"],
            create_time=TimeVO(time=row["create_time"]),
            update_time=UpdateableTime(time=row["update_time"]),
            target_time=SelectTime(row["target_time"]),
            post_id=PostId(idx=row["post_id"]),
            owner=self.user_repo.search_by_uid(
                Uid(idx=row["owner_id"])
            ).get_simple_user(),
            img_key=row["img_access_key"],
            share_flag=True if row["share_flag"] else False,
        )
        return a

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"

    def check_exist_pid(self, post_id: PostId) -> bool:
        connection = self.connect()
        table_name = self.get_padding_name("post")
        select_query = (
            f"SELECT post_id FROM {table_name} WHERE post_id = %s and delete_flag=0;"
        )
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

    def get_num_of_public_post(self) -> int:
        """_summary_
        공유 일기의 개수를 확인한다.

        Returns:
            int: _description_
        """
        raise NotImplementedError()

    def get_public_post_list(
        self,
        page: int = 0,
        posts_per_page: Optional[int] = None,
    ) -> Result[Collection[SimplePost]]:
        """_summary_
        공유 일기 리스트를 받아온다.

        Args:
            page (int, optional): _description_. Defaults to 0.
            posts_per_page (Optional[int], optional): 한번에 가져올 일기의 개수 정의, None은 모든 요소를 가져온다. Defaults to None.

        Returns:
            Result[Collection[SimplePost]]: _description_
        """
        connection = self.connect()
        table_name = self.get_padding_name("post")
        try:
            with connection.cursor() as cursor:
                # Execute the query with the given parameters
                query = f"""
SELECT post_id, title, target_time, share_flag, img_access_key, owner_id
FROM {table_name}
WHERE share_flag = 1 AND delete_flag = 0 
ORDER BY target_time DESC{ ";" if posts_per_page is None else '''
LIMIT %s OFFSET %s;''' }
            """
                match (posts_per_page, page):
                    case (None, any):
                        cursor.execute(query)
                    case (per, num) if per > 0 and num >= 0:
                        offset = (page) * posts_per_page
                        cursor.execute(query, (posts_per_page, offset))
                posts = cursor.fetchall()
                # 조회 결과를 SimplePost 객체로 매핑
                result_posts: List[SimplePost] = []
        except Exception as ex:
            connection.rollback()
            return Fail(type="Fail_Mysql_get_public_post_list_unknown")
        finally:
            connection.close()
        try:
            user_dict: Dict[int, SimpleUser] = {}

            for post in posts:
                own_id = post["owner_id"]
                if not own_id in user_dict.keys():
                    match self.user_repo.search_by_uid(Uid(own_id)):
                        case uservo if isinstance(uservo, UserVO):
                            user_dict[own_id] = uservo.get_simple_user()
                        case _:
                            ic("No User")
                            continue

                user = user_dict[own_id]
                share_flag = False if post["share_flag"] == 0 else True
                simple_post = SimplePost(
                    post_id=PostId(post["post_id"]),
                    title=post["title"],
                    target_time=SelectTime(post["target_time"]),
                    share_flag=share_flag,
                    img_key=post["img_access_key"],
                    owner=user,
                )
                result_posts.append(simple_post)
            return result_posts
        except:  # Exception as ex:
            return Fail(type="Fail_Mysql_get_public_post_list_unknown2")

    def search_by_available_pid(self, post_id: PostId) -> Optional[PostVO]:
        connection = self.connect()
        table_name = self.get_padding_name("post")

        try:
            with connection.cursor() as cursor:
                query = f"SELECT * FROM {table_name} WHERE post_id = %s AND delete_flag = 0;"
                cursor.execute(query, (post_id.idx))
                posts = cursor.fetchone()
                # 조회 결과를 SimplePost 객체로 매핑

                if posts:
                    return self._convert_to_postvo(posts)
        except Exception as ex:
            connection.rollback()
        finally:
            connection.close()

    def get_num_of_post_search_by_available_uid(self, user_id: Uid) -> int:
        """_summary_
        uid가 보유중인 사용가능한 일기의 개수를 가져온다.

        Args:
            user_id (Uid): _description_

        Returns:
            int: _description_
        """
        raise NotImplementedError()
        pass

    def search_by_available_uid(
        self,
        user_id: Uid,
        page: int = 0,
        posts_per_page: Optional[int] = None,
    ) -> Result[Collection[SimplePost]]:
        """_summary_
        uid를 기준으로 검색한다.
        단 삭제 플레그가 없는 사용가능한 일기만 가져온다.

        Args:
            user_id (Uid): _description_
            page (int, optional): _description_. Defaults to 0.
            posts_per_page (Optional[int], optional): 한번에 가져올 일기의 개수 정의, None은 모든 요소를 가져온다. Defaults to None.

        Returns:
            Result[Collection[SimplePost]]: _description_
        """
        connection = self.connect()
        table_name = self.get_padding_name("post")
        try:
            with connection.cursor() as cursor:
                # Execute the query with the given parameters
                query = f"""
SELECT post_id, title, target_time, share_flag, img_access_key, owner_id
FROM {table_name}
WHERE owner_id = %s AND delete_flag = 0 
ORDER BY target_time DESC{ ";" if posts_per_page is None else '''
LIMIT %s OFFSET %s;''' }
            """
                match (posts_per_page, page):
                    case (None, any):
                        cursor.execute(query, (user_id.idx))
                    case (per, num) if per > 0 and num >= 0:
                        offset = (page) * posts_per_page
                        cursor.execute(query, (user_id.idx, posts_per_page, offset))
                posts = cursor.fetchall()
                # 조회 결과를 SimplePost 객체로 매핑
                result_posts: List[SimplePost] = []
        except Exception as ex:
            connection.rollback()
            return Fail(type="Fail_Mysql_search_uid_post_list_unknown")
        finally:
            connection.close()
        try:
            user_dict: Dict[int, SimpleUser] = {}

            for post in posts:
                own_id = post["owner_id"]
                if not own_id in user_dict.keys():
                    match self.user_repo.search_by_uid(Uid(own_id)):
                        case uservo if isinstance(uservo, UserVO):
                            user_dict[own_id] = uservo.get_simple_user()
                        case _:
                            ic("No User")
                            continue

                user = user_dict[own_id]
                simple_post = SimplePost(
                    post_id=PostId(post["post_id"]),
                    title=post["title"],
                    target_time=SelectTime(post["target_time"]),
                    share_flag=False if post["share_flag"] == 0 else True,
                    img_key=post["img_access_key"],
                    owner=user,
                )
                result_posts.append(simple_post)
            return result_posts
        except:  # Exception as ex:
            return Fail(type="Fail_Mysql_search_uid_post_list_unknown2")

    def search_by_uid(
        self,
        user_id: Uid,
        page: int = 0,
        posts_per_page: Optional[int] = None,
    ) -> Result[Collection[SimplePost]]:
        """_summary_
        uid를 기준으로 모든 일기를 가져온다.

        Args:
            user_id (Uid): _description_

        Returns:
            Result[Collection[SimplePost]]: _description_
        """
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
