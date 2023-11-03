import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = str(now_path.parent)

if not (root_path in sys.path):
    sys.path.append(root_path)

from Commons.Types.ID import Id, Uid, UserId, UserIdVO, PostId
from Commons.Types.Content import Content
from Commons.Types.Password import Password

# __all__ = ["UserID", "Content", "Password"]
