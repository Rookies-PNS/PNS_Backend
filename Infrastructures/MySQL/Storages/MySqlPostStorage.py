import __init__

from Applications.Repositories.Interfaces import IPostRepository


class MySqlPostStorage(IPostRepository):
    def __init__(self, name_padding: str = "log_"):
        from get_db_data import get_mysql_dict

        self.name_padding = name_padding

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"
