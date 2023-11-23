import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Infrastructures.IOC.infra_factory import (
    get_user_storage,
    get_post_storage,
    get_strage_factory,
    select_strage,
    select_table_name_padding,
)
