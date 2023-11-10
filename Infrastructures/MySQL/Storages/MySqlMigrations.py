import __init__

from Infrastructures import IMigrations

import pymysql


class MySqlMigrations(IMigrations):
    def __init__(self):
        from get_db_data import get_mysql_dict

        sql_config = get_mysql_dict()
        self.conn = pymysql.connect(
            host=sql_config["host"],
            user=sql_config["user"],
            password=sql_config["password"],
            db=sql_config["database"],
            charset=sql_config["charset"],
        )

    def create_user(self):
        mycursor = self.conn.cursor()

        mycursor.execute(
            """
                        CREATE TABLE
                            id INT NOT NULL AUTO_INCREMENT,
                            account VARCHAR(100)  NOT NULL,
                            name VARCHAR(100) NOT NULL ,
                            pw VARCHAR(100) NOT NULL,
                         """
        )

    def init_user(self):
        raise NotImplementedError()

    def create_post(self):
        raise NotImplementedError()

    def init_post(self):
        raise NotImplementedError()
