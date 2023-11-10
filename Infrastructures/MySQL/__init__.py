import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = str(now_path.parent.parent)
print(root_path)

if not (root_path in sys.path):
    sys.path.append(root_path)


from Infrastructures.MySQL.MySqlFactory import MySqlFactory
