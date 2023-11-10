import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = str(now_path.parent.parent.parent)

if not (root_path in sys.path):
    sys.path.append(root_path)


from Infrastructures.MySQL.Storages.MySqlMigrations import MySqlMigrations
from Infrastructures.MySQL.Storages.MySqlPostStorage import MySqlPostStorage
from Infrastructures.MySQL.Storages.MySqlUserStorage import MySqlUserStorage
