from mysql_config import mysql_db


def get_mysql_url() -> str:
    return f"mysql://{mysql_db['user']}:{mysql_db['password']}@{mysql_db['host']}:{mysql_db['port']}/{mysql_db['database']}?charset={mysql_db['charset']}"


def get_mysql_dict() -> dict:
    return mysql_db
