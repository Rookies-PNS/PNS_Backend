import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = str(now_path.parent.parent)

if not (root_path in sys.path):
    sys.path.append(root_path)

from Applications.Repositories.Queries.IPostQuery import IPostQurey
from Applications.Repositories.Queries.IOperation import *
