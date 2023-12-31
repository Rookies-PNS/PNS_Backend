import __init__
from typing import Optional

from Commons import *
from Domains.Entities import User, UserVO, SimpleUser, SecuritySimpleUser
from Applications.Results import Result, Fail, Fail_CreateUser_IDAlreadyExists
from Applications.Repositories.Interfaces import IUserWriteableRepository

import pymysql

# from icecream import ic


class MySqlUserWriteStorage(IUserWriteableRepository):
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

    def check_exist_userid(self, userid: str) -> bool:
        """_summary_
        userid를 통해서 저장소에 존재하는지 여부를 알 수 있다.

        Args:
            userid (str): _description_

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

    def save_user(self, user: User) -> Optional[Fail]:
        """_summary_
        사용자를 저장한다.

        Args:
            user (User): _description_

        Returns:
            Optional[Fail]: 성공시 None 반환, 실패시 Fail반환
        """
        connection = self.connect()
        user_table_name = self.get_padding_name("user")
        auth_table_name = self.get_padding_name("user_auth")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # 데이터 삽입 쿼리
                insert_query = insert_user_query = f"""
INSERT INTO {user_table_name} (
    pw,
    account,
    name,
    nickname, 
    time_of_try_login,
    lock_flag,
    count_of_login_fail,
    post_last_update_date,
    post_num
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(
                    insert_query,
                    (
                        user.get_passwd(),
                        user.get_account(),
                        user.get_user_name(),
                        user.get_user_nickname(),
                        user.get_time_of_try_login(),
                        user.get_lock_flag(),
                        user.get_count_of_login_fail(),
                        user.post_count.last_update_date.get_time(),
                        user.get_post_num(),
                    ),
                )
                insert_query = f"""INSERT INTO {auth_table_name} (policy, scope, account) VALUES (%s, %s, %s);"""

                for auth in user.auth.auths:
                    cursor.execute(
                        insert_query,
                        (
                            auth.policy.value,
                            auth.scope.value,
                            user.get_account(),
                        ),
                    )

                # 변경 사항을 커밋
                connection.commit()
        except:
            connection.rollback()
            return Fail(type="Mysql_Fail_SaveUser_Query_Error")
        finally:
            # 연결 닫기
            connection.close()
        if self.check_exist_userid(user.get_account()):
            return None
        return Fail(type="Mysql_Fail_SaveUser_Not_Found")

    def update_all(self, user: UserVO) -> Optional[Fail]:
        """_summary_
        사용자 정보를 갱신한다.

        Args:
            user (UserVO): _description_

        Returns:
            Result[Uid]: _description_
        """
        raise NotImplementedError()

    def update_auth(self, user: SecuritySimpleUser) -> Optional[Fail]:
        """_summary_
        사용자의 권한정보를 갱신한다.

        Args:
            user (SimpleUser): _description_

        Returns
            Optional[Fail]: None 이면 성공, Fail이면 실패
        """

        raise NotImplementedError()

    def update_post_counter(self, user: SimpleUser) -> Result[int]:
        """_summary_
        사용자의 마지막 일기 수정일 갱신과 마지막날 작성한 일기의 개수를 카운트 한다.
        현재 날짜와 수정일이 같으면 카운트는 증가하고,
        현재 날짜와 수정일이 다르면 카운트는 1로 수정일은 현재 날짜로 갱신된다.

        Args:
            user (SimpleUser): _description_

        Returns:
            Result[int]: 당일 일기 작성 개수
        """

        raise NotImplementedError()

    def update_to_fail_login(self, user: SimpleUser, lock_flag: bool) -> Result[int]:
        """_summary_
        로그인을 실패한 것으로 업데이트 한다.

        Args:
            user (SimpleUser): _description_
            lock_flag (bool): _description_

        Returns:
            Result[int]: 로그인 실패 횟수
        """
        from datetime import datetime

        connection = self.connect()
        user_table_name = self.get_padding_name("user")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블 생성 쿼리
                update_query = f"""
UPDATE {user_table_name}
SET time_of_try_login = %s, lock_flag = %s, count_of_login_fail = {user_table_name}.count_of_login_fail + 1
WHERE id = %s;
                """
                # 데이터베이스에 쿼리 실행
                cursor.execute(
                    update_query, (datetime.now(), lock_flag, user.get_uid().idx)
                )
                # 커밋
                connection.commit()
        except Exception as ex:
            # 트랜잭션 롤백
            connection.rollback()
            raise ex

        finally:
            # 연결 닫기
            connection.close()

    def update_to_success_login(self, user: SimpleUser) -> Optional[Fail]:
        """_summary_
        로그인을 성공한 것으로 업데이트 한다.

        Args:
            user (SimpleUser): _description_

        Returns:
            Optional[Fail]: None 이면 성공, Fail이면 실패
        """
        from datetime import datetime

        connection = self.connect()
        user_table_name = self.get_padding_name("user")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블 생성 쿼리
                update_query = f"""
UPDATE {user_table_name}
SET time_of_try_login = %s, lock_flag = %s, count_of_login_fail = %s
WHERE id = %s;
                """
                # 데이터베이스에 쿼리 실행
                cursor.execute(
                    update_query, (datetime.now(), False, 0, user.get_uid().idx)
                )

                # 커밋
                connection.commit()
        except Exception as ex:
            # 트랜잭션 롤백
            connection.rollback()
            raise ex

        finally:
            # 연결 닫기
            connection.close()

    def delete(self, user: SimpleUser) -> Result[Uid]:
        """_summary_
        사용자의 정보를 삭제(비공개) 처리한다.

        Args:
            user (SimpleUser): _description_

        Returns:
            Result[Uid]: _description_
        """

        raise NotImplementedError()
