import __init__
from collections.abc import Collection
from typing import Optional
from abc import *

from Domains.Entities import PostVO


class IConditionRanderForPostQurey(metaclass=ABCMeta):
    @abstractmethod
    def query(self) -> Collection[PostVO]:
        pass
