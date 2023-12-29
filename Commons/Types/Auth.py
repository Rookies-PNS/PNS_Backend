from dataclasses import dataclass
from enum import Enum, auto
from typing import List


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


class TargetScope(Enum):
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
    target_range: TargetScope


@dataclass
class AuthArchives:
    auths: List[Auth]

    def check_policy(self, policy: Policy) -> List[TargetScope]:
        """_summary_
        정책(policy)을 소유여 부를 확인하고, 유효범위(TargetRange)를 반환한다.

        Args:
            policy (Policy): 알고자 하는 정책

        Returns:
            List[TargetRange]: 정책이 같은 모든 유효범위 반환(TargetScope), 없으면 empty list 반환
        """
        scopes: List[TargetScope] = []
        for auth in self.auths:
            if auth.policy == policy:
                scopes.append(auth.target_range)

        return scopes


@dataclass
class UnionPolicy:
    auths: List[Policy]


@dataclass
class IntersectionPolicy:
    auths: List[Policy]
