import __init__
from typing import Optional

from Commons import Uid, UserId, Password
from Domains.Entities import User, UserVO
from Applications.Results import Result, Fail, Fail_CreateUser_IDAlreadyExists
from Applications.Repositories.Interfaces import IUserRepository

import pymysql


class MySqlUserStorage(IUserRepository):
    def __init__(self, name_padding: str = "log_"):
        from get_db_data import get_mysql_dict

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

    def save(self, user: User) -> Result[UserVO]:
        connection = self.connect()
        table_name = self.get_padding_name("user")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # 데이터 삽입 쿼리
                insert_query = (
                    f"INSERT INTO {table_name} (pw, account, name) VALUES (%s, %s, %s);"
                )
                result = cursor.execute(
                    insert_query,
                    (user.password.pw, user.user_id.account, user.name),
                )
            # 변경 사항을 커밋
            connection.commit()
        except:
            return Fail(type="MysqlFailSaveUser")
        finally:
            # 연결 닫기
            connection.close()

        ret = self.search_by_userid(user.user_id)

        match ret:
            case _ if isinstance(ret, UserVO):
                return ret
            case _:
                return Fail(type="MysqlNotSaveUser")

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
                        user_id=UserId(account=result[2]),
                        name=result[3],
                        password=Password(pw=result[1]),
                        uid=Uid(idx=result[0]),
                    )

        finally:
            # 연결 닫기
            connection.close()
            return ret

    def search_by_userid(self, userid: UserId) -> Optional[UserVO]:
        connection = self.connect()
        table_name = self.get_padding_name("user")
        ret: Optional[UserVO] = None
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # 계정 검색 쿼리
                select_query = f"SELECT * FROM {table_name} WHERE account = %s;"

                cursor.execute(select_query, (userid.account,))

                # 결과 가져오기
                result = cursor.fetchone()

                if result:
                    ret = UserVO(
                        user_id=UserId(account=result[2]),
                        name=result[3],
                        password=Password(pw=result[1]),
                        uid=Uid(idx=result[0]),
                    )
        except Exception as ex:
            connection.rollback()

        finally:
            # 연결 닫기
            connection.close()
            return ret

    def update(self, user: UserVO) -> Result[UserVO]:
        raise NotImplementedError()

    def delete(self, user: UserVO) -> Result[Uid]:
        raise NotImplementedError()
