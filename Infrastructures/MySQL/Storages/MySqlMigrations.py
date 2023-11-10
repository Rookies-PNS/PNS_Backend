import __init__
from collections.abc import Collection

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
        table_name = self.get_padding_name("user")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블 생성 쿼리
                create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pw VARCHAR(255) NOT NULL,
    account VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL
);
                """
                cursor.execute(create_table_query)

            # 변경 사항을 커밋
            connection.commit()

        finally:
            # 연결 닫기
            connection.close()

    def init_user(self, init_users: Collection[UserVO] = []):
        connection = self.connect()
        table_name = self.get_padding_name("user")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # 데이터 삽입 쿼리
                insert_query = (
                    f"INSERT INTO {table_name} (pw, account, name) VALUES (%s, %s, %s);"
                )
                for user in init_users:
                    cursor.execute(
                        insert_query,
                        (user.password.pw, user.user_id.account, user.name),
                    )

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
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES {table_user}(id)
);
                """
                cursor.execute(create_table_query)

            # 변경 사항을 커밋
            connection.commit()

        finally:
            # 연결 닫기
            connection.close()

    def init_post(self, init_posts: Collection[PostVO] = []):
        connection = self.connect()
        table_name = self.get_padding_name("post")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # 데이터 삽입 쿼리
                insert_query = f"INSERT INTO {table_name} (title, content, user_id) VALUES (%s, %s, %s);"
                for post in init_posts:
                    cursor.execute(
                        insert_query,
                        (post.title, post.content, post.user_id),
                    )

            # 변경 사항을 커밋
            connection.commit()

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
