import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parent.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Applications.Usecases.PostServices.CreatePostService import CreatePostService
from Applications.Usecases.PostServices.DeletePostService import DeletePostService
from Applications.Usecases.PostServices.GetPrivatePostService import (
    GetPrivatePostService,
)
from Applications.Usecases.PostServices.GetPublicPostService import GetPublicPostService
from Applications.Usecases.PostServices.UpdatePostService import UpdatePostService
