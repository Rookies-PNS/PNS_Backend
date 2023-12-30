import __init__
import unittest
import sys
from datetime import datetime, timedelta

from Domains.Entities import User, SimpleUser, SecuritySimpleUser
from Commons import (
    Uid,
    UserId,
    AuthArchives,
    Auth,
    Policy,
    TargetScope,
    UnionPolicy,
    IntersectionPolicy,
)
from icecream import ic


class test_user(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_auth)")
        cls.일반사용자_auths = [
            Auth(Policy.UserDataReadAblePolicy, TargetScope.Own),  # 자신의 유저 정보 열람가능
            Auth(Policy.UserDataDeleteAblePolicy, TargetScope.Own),  # 자기 계정 삭제가능
            Auth(Policy.PostReadAblePolicy, TargetScope.Allowed),  # 공개된 일기 읽기 가능
            Auth(Policy.PostReadAblePolicy, TargetScope.Own),  # 자기 일기 읽기 가능
            Auth(Policy.PostDeleteAblePolicy, TargetScope.Own),  # 자기 일기 삭제가능
            Auth(Policy.PostCreateAndUpdateAblePolicy, TargetScope.Own),  # 자기 일기 수정가능
            Auth(Policy.PostPublicAblePolicy, TargetScope.Own),  # 자기 일기 공개가능
            Auth(Policy.PostPrivateAblePolicy, TargetScope.Own),  # 자기 일기 비공개가능
        ]
        cls.공유일기관리자_auths = [
            Auth(Policy.PostReadAblePolicy, TargetScope.Allowed),  # 공개된 일기 읽기 가능
            Auth(Policy.UserDataReadAblePolicy, TargetScope.Own),  # 자신의 유저 정보 열람가능
            Auth(Policy.PostPrivateAblePolicy, TargetScope.All),  # 모든 일기 비공개가능
            Auth(
                Policy.UserAuthLockOfPostPublicPolicy, TargetScope.All
            ),  # 모든 유저 일기공개 권한정지 권한
            Auth(
                Policy.UserAuthUnlockOfPostPublicPolicy, TargetScope.All
            ),  # 모든 유저 일기공개 권한정지 해제 권한
            Auth(Policy.UserDataReadAblePolicy, TargetScope.All),  # 모든 유저 정보 열람가
            Auth(Policy.UserDataDeleteAblePolicy, TargetScope.Own),  # 자기 계정 삭제가능
        ]
        cls.계정관리자_auths = [
            Auth(Policy.PostReadAblePolicy, TargetScope.Allowed),  # 공개된 일기 읽기 가능
            Auth(Policy.UserDataReadAblePolicy, TargetScope.Own),  # 자신의 유저 정보 열람가능
            Auth(Policy.PostDeleteAblePolicy, TargetScope.All),  # All 일기 삭제가능
            Auth(
                Policy.UserAuthLockOfPostCreateAndUpdatePolicy, TargetScope.All
            ),  # 일기 쓰기 권한정지 권한
            Auth(
                Policy.UserAuthUnlockOfPostCreateAndUpdatePolicy, TargetScope.All
            ),  # 일기 쓰기 권한정기 해제 권한
            Auth(Policy.UserDataReadAblePolicy, TargetScope.All),  # 모든 유저 정보 열람가능
            Auth(Policy.UserDataDeleteAblePolicy, TargetScope.All),  # 모든 계정 삭제가능
        ]

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)

    def test_계정관리자_delete_user_policy(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        계정관리자_archives = AuthArchives(self.계정관리자_auths)
        require_policy = IntersectionPolicy(
            policies=[
                Policy.PostDeleteAblePolicy,
                Policy.UserDataDeleteAblePolicy,
            ]
        )

        # 소유 계정 삭제
        self.assertTrue(
            require_policy.chcek_auth(
                actor_auth_Archives=계정관리자_archives,
                actor_uid=Uid(idx=1),
                target_owner_id=Uid(idx=1),
            )
        )
        # 타인 계정 삭제
        self.assertTrue(
            require_policy.chcek_auth(
                actor_auth_Archives=계정관리자_archives,
                actor_uid=Uid(idx=1),
                target_owner_id=Uid(idx=2),
            )
        )

    def test_일반사용자_delete_user_policy(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        일반사용자_archives = AuthArchives(self.일반사용자_auths)
        require_policy = IntersectionPolicy(
            policies=[
                Policy.PostDeleteAblePolicy,
                Policy.UserDataDeleteAblePolicy,
            ]
        )

        # 소유 계정 삭제
        self.assertTrue(
            require_policy.chcek_auth(
                actor_auth_Archives=일반사용자_archives,
                actor_uid=Uid(idx=1),
                target_owner_id=Uid(idx=1),
            )
        )
        # 타인 계정 삭제
        self.assertFalse(
            require_policy.chcek_auth(
                actor_auth_Archives=일반사용자_archives,
                actor_uid=Uid(idx=1),
                target_owner_id=Uid(idx=2),
            )
        )


def main():
    unittest.main()


if __name__ == "__main__":
    main()
