import __init__
from collections.abc import Collection

from Commons import Policy, TargetScope
from Applications.Repositories.Interfaces import IMigrations
from Domains.Entities import UserVO, PostVO

import pymysql


class MySqlMigrations(IMigrations):
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

    def create_user(self):
        connection = self.connect()
        user_table_name = self.get_padding_name("user")
        auth_table_name = self.get_padding_name("user_auth")

        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # 트랜잭션 시작
                cursor.execute("START TRANSACTION;")

                # "users" 테이블 생성 쿼리
                create_table_query = f"""
CREATE TABLE IF NOT EXISTS {user_table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pw VARCHAR(511) NOT NULL,
    account VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL
    nickname VARCHAR(50),
    time_of_try_login DATETIME,
    lock_flag BOOLEAN,
    count_of_login_fail INT,
    post_last_update_date DATETIME,
    post_num INT
);
                """
                # user 생성
                cursor.execute(create_table_query)

                policy = ", ".join(
                    list(map(lambda x: f"'{x}'", Policy.__members__.keys()))
                )
                scope = ", ".join(
                    list(map(lambda x: f"'{x}'", TargetScope.__members__.keys()))
                )
                # UserAuth 테이블 생성 쿼리
                create_auth_table_query = f"""
CREATE TABLE IF NOT EXISTS {auth_table_name} (
    auth_id INT AUTO_INCREMENT PRIMARY KEY,
    policy ENUM({policy}) NOT NULL,
    scope ENUM({scope})) NOT NULL,
    user_account VARCHAR(50),
    FOREIGN KEY (user_account) REFERENCES users(user_account)
);
"""

            # 변경 사항을 커밋
            connection.commit()

        finally:
            # 연결 닫기
            connection.close()

    def delete_user(self):
        connection = self.connect()
        table_name = self.get_padding_name("user")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블 삭제 쿼리
                drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
                cursor.execute(drop_table_query)

            # 변경 사항을 커밋
            connection.commit()

        finally:
            # 연결 닫기
            connection.close()

    def check_exist_user(self) -> bool:
        connection = self.connect()
        table_name = self.get_padding_name("user")
        ret = False
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블이 존재하는지 확인하는 쿼리 실행
                table_exists_query = f"SHOW TABLES LIKE '{table_name}';"
                cursor.execute(table_exists_query)

                # 결과 가져오기
                result = cursor.fetchone()

                if result:
                    ret = True
        finally:
            # 연결 닫기
            connection.close()
            return ret

    def create_post(self):
        from icecream import ic

        connection = self.connect()
        table_name = self.get_padding_name("post")
        table_user = self.get_padding_name("user")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "post" 테이블 생성 쿼리
                create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES {table_user}(id)
);
                """
                cursor.execute(create_table_query)

            # 변경 사항을 커밋
            connection.commit()
        except:
            connection.rollback()
        finally:
            # 연결 닫기
            connection.close()

    def delete_post(self):
        connection = self.connect()
        table_name = self.get_padding_name("post")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블 삭제 쿼리
                drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
                cursor.execute(drop_table_query)

            # 변경 사항을 커밋
            connection.commit()
        finally:
            # 연결 닫기
            connection.close()

    def check_exist_post(self) -> bool:
        connection = self.connect()
        table_name = self.get_padding_name("post")
        ret = False
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블이 존재하는지 확인하는 쿼리 실행
                table_exists_query = f"SHOW TABLES LIKE '{table_name}';"
                cursor.execute(table_exists_query)

                # 결과 가져오기
                result = cursor.fetchone()

                if result:
                    ret = True
        finally:
            # 연결 닫기
            connection.close()
            return ret
