import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Applications.Repositories.Interfaces.IPostWriteableRepository import (
    IPostWriteableRepository,
)
from Applications.Repositories.Interfaces.IPostReadableRepository import (
    IPostReadableRepository,
)
from Applications.Repositories.Interfaces.IUserWriteableRepository import (
    IUserWriteableRepository,
)
from Applications.Repositories.Interfaces.IUserReadableRepository import (
    IUserReadableRepository,
)
from Applications.Repositories.Interfaces.IMigrations import IMigrations

from Applications.Repositories.Interfaces.IImageSaveableRepository import (
    IImageSaveableRepository,
)
from Applications.Repositories.Interfaces.IImageDeleteableRepository import (
    IImageDeleteableRepository,
)
from Applications.Repositories.Interfaces.IImageDataReadableRepository import (
    IImageDataReadableRepository,
)
