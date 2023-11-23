import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Domains.Entities.Post import Post, PostVO, SimplePost, Post_to_PostVO, PostVO_to_Post
from Domains.Entities.User import User, UserVO, SimpleUser
