import __init__
from collections.abc import Collection
from typing import Optional
from abc import *

from Domains.Entities import PostVO


class IPostQurey(metaclass=ABCMeta):
    @abstractmethod
    def query(self, oper: Optional[str] = None) -> Collection[PostVO]:
        pass
