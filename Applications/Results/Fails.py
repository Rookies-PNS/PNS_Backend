import __init__
from dataclasses import dataclass

from Applications.Results.Result import Fail


@dataclass(frozen=True)
class Fail_CreateUser_IDAlreadyExists(Fail):
    type: str = "IDAlreadyExists"


@dataclass(frozen=True)
class Fail_CheckUser_IDNotFound(Fail):
    type: str = "IDNotFound"


@dataclass(frozen=True)
class Fail_CheckUser_PasswardNotCorrect(Fail):
    type: str = "PasswardNotCorrect"
