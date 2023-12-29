import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parent.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Applications.Usecases.PostServices.CreatePostService import CreatePost
from Applications.Usecases.PostServices.DeletePostService import DeletePost
from Applications.Usecases.PostServices.GetPrivatePostService import GetPostDetail
from Applications.Usecases.PostServices.GetPublicPostService import GetPostDetail
from Applications.Usecases.PostServices.UpdatePostService import UpdateableTime
