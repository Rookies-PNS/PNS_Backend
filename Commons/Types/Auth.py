from dataclasses import dataclass
from abc import *
from enum import Enum, auto
from typing import List

from Commons import Uid

from icecream import ic


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
    # Borrow = auto()
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


class ICheckPolicy(metaclass=ABCMeta):
    @abstractmethod
    def chcek_auth(
        self,
        actor_auth_Archives: AuthArchives,
        actor_uid: Uid,
        target_owner_id: Uid,
        taget_allow_flag: bool = False,
    ) -> bool:
        """_summary_
        actor가 target을 사용할 수 있는 권한을 가졌는지 판단해 준다.

        Args:
            actor_auth_Archives (AuthArchives):
            actor_uid (Uid): actor
            target_owner_id (Uid): Uid / target identity
            taget_allow_flag (bool, optional): target 허용 여부. Defaults to False.

        Returns:
            bool: True (Able) / False (UnAble)
        """
        pass

    def check_scope(
        self,
        actor_uid: Uid,
        actor_scope: TargetScope,
        target_owner_id: Uid,
        target_allow_flag: bool,
    ) -> bool:
        """_summary_
        actor가 target을 사용할 수 있는 범위인지 판단해준다.

        Args:
            actor_uid (Uid): actor  identity
            actor_scope (TargetScope): actor scope of policy
            target_owner_id (Uid): Uid / target identity
            taget_allow_flag (bool, optional): target 허용 여부.

        Returns:
            bool: True (Able) / False (UnAble)
        """

        match actor_scope.value:
            case TargetScope.All.value:
                return True
            case TargetScope.Allowed.value:
                return target_allow_flag
            case TargetScope.Own.value:
                return actor_uid == target_owner_id


@dataclass
class UnionPolicy(ICheckPolicy):
    """_summary_
    등록된 정책 중 하나라도 가지면, 허용하는 정책
    """

    policies: List[Policy]

    def check_auth(
        self,
        actor_auth_Archives: AuthArchives,
        actor_uid: Uid,
        target_owner_id: Uid,
        taget_allow_flag: bool = False,
    ) -> bool:
        """_summary_
        actor가 target을 사용할 수 있는 권한을 가졌는지 판단해 준다.

        Args:
            actor_auth_Archives (AuthArchives):
            actor_uid (Uid): actor
            target_owner_id (Uid): Uid / target identity
            taget_allow_flag (bool, optional): target 허용 여부. Defaults to False.

        Returns:
            bool: True (Able) / False (UnAble)
        """
        for policy in self.policies:
            scopes = actor_auth_Archives.check_policy(policy)
            for scope in scopes:
                if self.check_scope(
                    actor_uid, scope, target_owner_id, taget_allow_flag
                ):
                    return True
        return False


@dataclass
class IntersectionPolicy(ICheckPolicy):
    """_summary_
    등록된 정책 모두를 가지면, 허용되는 정책
    """

    policies: List[Policy]

    def chcek_auth(
        self,
        actor_auth_Archives: AuthArchives,
        actor_uid: Uid,
        target_owner_id: Uid,
        taget_allow_flag: bool = False,
    ) -> bool:
        """_summary_
        actor가 target을 사용할 수 있는 권한을 가졌는지 판단해 준다.

        Args:
            actor_auth_Archives (AuthArchives):
            actor_uid (Uid): actor
            target_owner_id (Uid): Uid / target identity
            taget_allow_flag (bool, optional): target 허용 여부. Defaults to False.

        Returns:
            bool: True (Able) / False (UnAble)
        """
        for policy in self.policies:
            scopes = actor_auth_Archives.check_policy(policy)
            flag = False
            for scope in scopes:
                if self.check_scope(
                    actor_uid, scope, target_owner_id, taget_allow_flag
                ):
                    flag = True
                    break
            if not flag:  # have not Auth
                return False
        return True
