import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = str(now_path.parent.parent)

if not (root_path in sys.path):
    sys.path.append(root_path)

from Applications.Repositories.Interfaces.IPostRepository import IPostRepository
from Applications.Repositories.Interfaces.IUserRepository import IUserRepository
from Applications.Repositories.Interfaces.IMigrations import IMigrations
