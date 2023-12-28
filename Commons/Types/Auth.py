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
    UserAuthLockOfPostPublicPolicy = auto()
    UserAuthUnlockOfPostPublicPolicy = auto()
    # UserLoginUnlockAblePolicy = auto()
    UserDataReadAblePolicy = auto()
    UserDataDeleteAblePolicy = auto()


class TargetRange(Enum):
    """_summary_

    Args:
        Enum (All): 어떤 범위가 와도 인정된다.
    """

    Own = auto()
    Borrow = auto()
    Allowed = auto()
    All = auto()  # 어떤 범위가 와도 인정된다.


@dataclass(frozen=True)
class Auth:
    policy: Policy
    target_range: TargetRange


@dataclass
class AuthArchives:
    auths: List[Auth]

    def check_get_auth(self, auth: Auth) -> bool:
        """_summary_
        auth(인자)권한을 소유하고 있는지를 반환한다.


        Args:
            auth (Auth):

        Returns:
            bool: True(해당 권한을 가짐), False(권한 없음)
        """
        for item in self.auths:
            if item.policy != auth.policy:
                continue
            if item.target_range == auth.target_range:
                return True
            # 어떤 범위가 와도 인정된다.
            if item.target_range == TargetRange.All:
                return True

        return False


@dataclass
class UnionAuth:
    auths: List[Auth]


@dataclass
class IntersectionAuth:
    auths: List[Auth]
