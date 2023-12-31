import __init__
from typing import Optional
from collections.abc import Collection

# from datetime import datetime

from Commons import *
from Domains.Entities import User, UserVO, SimpleUser, SecuritySimpleUser
from Applications.Results import Result, Fail, Fail_CreateUser_IDAlreadyExists
from Applications.Repositories.Interfaces import IUserReadableRepository

import pymysql

# from icecream import ic


class MySqlUserReadStorage(IUserReadableRepository):
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
            cursorclass=pymysql.cursors.DictCursor,
        )

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"

    def check_exist_userid(self, userid: str) -> bool:
        connection = self.connect()
        table_name = self.get_padding_name("user")
        ret = False
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # 계정 검색 쿼리
                select_query = f"SELECT * FROM {table_name} WHERE account = %s;"
                cursor.execute(select_query, (userid,))

                # 결과 가져오기
                result = cursor.fetchone()

                if result:
                    ret = True

        finally:
            # 연결 닫기
            connection.close()
            return ret

    def search_by_uid(self, uid: Uid) -> Optional[UserVO]:
        connection = self.connect()
        table_name = self.get_padding_name("user")
        ret: Optional[UserVO] = None
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # 계정 검색 쿼리
                select_query = f"SELECT * FROM {table_name} WHERE id = %s;"
                cursor.execute(select_query, (uid.idx,))

                # 결과 가져오기
                result = cursor.fetchone()

                if result:
                    ret = UserVO(
                        user_account=UserId(account=result[2]),
                        name=result[3],
                        password=Password(pw=result[1]),
                        uid=Uid(idx=result[0]),
                    )
        except:
            connection.rollback()

        finally:
            # 연결 닫기
            connection.close()
            return ret

    def search_by_userid(self, userid: str) -> Optional[SimpleUser]:
        connection = self.connect()
        user_table_name = self.get_padding_name("user")
        auth_table_name = self.get_padding_name("user_auth")
        ret: Optional[UserVO] = None
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # 계정 검색 쿼리
                select_query = f"""
SELECT account, nickname, id, post_last_update_date, post_num FROM {user_table_name} WHERE account = %s;"""

                cursor.execute(select_query, (userid,))

                # 결과 가져오기
                user_result = cursor.fetchone()

                # 계정 검색 쿼리
                select_query = (
                    f"SELECT policy, scope FROM {auth_table_name} WHERE account = %s;"
                )

                cursor.execute(select_query, (userid,))

                # 결과 가져오기
                auth_result = cursor.fetchall()
                auths = [
                    Auth(
                        policy=Policy[auth["policy"]], scope=TargetScope[auth["scope"]]
                    )
                    for auth in auth_result
                ]

                if user_result:
                    ret = SimpleUser(
                        user_account=UserId(account=user_result["account"]),
                        nickname=user_result["nickname"],
                        uid=Uid(idx=user_result["id"]),
                        auth=AuthArchives(auths=auths),
                        post_count=PostCounter(
                            last_update_date=UpdateableTime(
                                user_result["post_last_update_date"]
                            ),
                            post_num=user_result["post_num"],
                        ),
                    )
        except:
            connection.rollback()

        finally:
            # 연결 닫기
            connection.close()
            return ret

    def get_num_of_security_user(self) -> int:
        """_summary_
        유효한 시큐리티 사용자 계정의 총 수를 반환합니다.
        Returns:
            int: 검색된 인원수
        """
        raise NotImplementedError()

    def get_security_user_list(
        self,
        page: int = 0,
        posts_per_page: Optional[int] = None,
    ) -> Optional[Collection[SecuritySimpleUser]]:
        """_summary_
        Args:
            user_id (Uid): _description_
            page (int, optional): _description_. Defaults to 0.
            posts_per_page (Optional[int], optional): 한번에 가져올 일기의 개수 정의, None은 모든 요소를 가져온다. Defaults to None.

        Returns:
            Optional[Collection[SimplePost]]: _description_
        """
        raise NotImplementedError()

    def get_login_data(self, user_id: str) -> Optional[LoginData]:
        """_summary_
        사용자의 로그인 실패 현황을 받아온다.

        Args:
            user_id (str): _description_

        Returns:
            Optional[LoginData]: _description_
        """
        connection = self.connect()
        table_name = self.get_padding_name("user")
        ret: Optional[LoginData] = None
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # 계정 검색 쿼리
                select_query = f"SELECT time_of_try_login, lock_flag, count_of_login_fail  FROM {table_name} WHERE account = %s;"
                cursor.execute(select_query, (user_id,))

                # 결과 가져오기
                result = cursor.fetchone()

                if result:
                    ret = LoginData(
                        time_of_try_login=UpdateableTime(result["time_of_try_login"]),
                        lock_flag=result["lock_flag"],
                        count_of_login_fail=result["count_of_login_fail"],
                    )
        except Exception as ex:
            connection.rollback()

        finally:
            # 연결 닫기
            connection.close()
            return ret

    def compare_pw(self, user_id: str, pw: Password) -> bool:
        """_summary_
        유저의 패스워드를 비교해서 결과를 반환해 준다.

        Args:
            user (SimpleUser): _description_
            pw (Password): _description_

        Returns:
            bool: _description_
        """
        connection = self.connect()
        table_name = self.get_padding_name("user")
        ret = False
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # 계정 검색 쿼리
                select_query = (
                    f"SELECT 1 FROM {table_name} WHERE account = %s AND pw = %s;"
                )
                cursor.execute(select_query, (user_id, pw.pw))

                # 결과 가져오기
                result = cursor.fetchone()
                if result:
                    ret = True
        except:
            pass
        finally:
            # 연결 닫기
            connection.close()
        return ret
