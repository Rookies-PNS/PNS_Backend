import __init__

from Infrastructures.Migrations import IMigrations


import pymysql


class MySqlMigrations(IMigrations):
    def __init__(self):
        from get_db_data import get_mysql_dict

        sql_config = get_mysql_dict()
        conn = pymysql.connect(
            host=sql_config["host"],
            user=sql_config["user"],
            password=sql_config["password"],
            db=sql_config["database"],
            charset=sql_config["charset"],
        )

    def create_user(self):
        ...

    def init_user(self):
        ...

    def create_post(self):
        ...

    def init_post(self):
        ...
