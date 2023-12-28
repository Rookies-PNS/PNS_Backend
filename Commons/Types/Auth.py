from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Union


class Policy(Enum):
    none = auto()
    PostCreateAndUpdateAblePolicy = auto()
    PostReadAblePolicy = auto()
    PostDeleteAblePolicy = auto()
    PostPublicAblePolicy = auto()
    PostPrivateAblePolicy = auto()
    UserAuthLockOfPostCreateAndUpdatePolicy = auto()
    UserAuthUnlockOfPostCreateAndUpdatePolicy = auto()
    UserLoginUnlockAblePolicy = auto()
    UserDataReadAblePolicy = auto()
    UserDataDeleteAblePolicy = auto()


class TargetRange(Enum):
    Own = auto()
    Borrow = auto()
    Allowed = auto()
    All = auto()


@dataclass(frozen=True)
class Auth:
    policy: Policy
    target_range: TargetRange


@dataclass
class AuthArchives:
    auths: List[Auth]


@dataclass
class UnionAuth:
    auths: List[Auth]


@dataclass
class IntersectionAuth:
    auths: List[Auth]
