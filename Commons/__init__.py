import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Commons.Types.ID import Id, Uid, UserId, PostId
from Commons.Types.Content import Content
from Commons.Types.Password import Password
from Commons.Types.Time import PostCreateTime, PostUpdateTime, get_current_time

# __all__ = ["UserID", "Content", "Password"]
