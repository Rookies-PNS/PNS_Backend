import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parent.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))


from Infrastructures.MySQL.Storages.MySqlMigrations import MySqlMigrations
from Infrastructures.MySQL.Storages.MySqlPostWriteStorage import MySqlPostWriteStorage
from Infrastructures.MySQL.Storages.MySqlPostReadStorage import MySqlPostReadStorage
from Infrastructures.MySQL.Storages.MySqlUserWriteStorage import MySqlUserWriteStorage
from Infrastructures.MySQL.Storages.MySqlUserReadStorage import MySqlUserReadStorage
