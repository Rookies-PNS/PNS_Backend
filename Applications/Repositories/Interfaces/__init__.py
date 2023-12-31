import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Applications.Repositories.Interfaces.IPostRepository import IPostRepository
from Applications.Repositories.Interfaces.IUserRepository import IUserRepository
from Applications.Repositories.Interfaces.IMigrations import IMigrations
from Applications.Repositories.Interfaces.SessionRepository import SessionRepository
