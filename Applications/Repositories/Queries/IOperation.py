import __init__
from abc import *
from dataclasses import dataclass
from enum import Enum, auto


class SortOperation(Enum):
    asc = auto()
    des = auto()


class NumbericOperation(Enum):
    gt = auto()
    ge = auto()
    lt = auto()
    le = auto()
    eq = auto()
    ne = auto()


class IOperation(metaclass=ABCMeta):
    def get_str_oper(target: str) -> str:
        pass
