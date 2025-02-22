import __init__
import unittest
import sys
from typing import List, Tuple

from Commons import *
from Domains.Entities import UserVO, SimpleUser
from Applications.Usecases.UserServices import CreateUserService, LoginService
from Applications.Usecases.UserServices.UsecaseUserExtention import (
    convert_to_Password_with_hashing,
    get_padding_adder,
)
from Applications.Results import (
    Fail,
    Fail_CheckUser_IDNotFound,
    Fail_CreateUser_IDAlreadyExists,
)

import Tests.Applications.Usecases.storage_selecter as test_selector
from icecream import ic


class test_user_services(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name)
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
        factory = test_selector.get_test_factory("user_service_test_")

        migrate = test_selector.get_usecase_migration(factory)
        # 깔끔하게 지우고 시작
        if migrate.check_exist_user():
            migrate.delete_user()
        # 테이블 생성
        migrate.create_user()

        # 기본세팅
        repoW, repoR = test_selector.get_user_storage(factory)
        create_user_service = CreateUserService(repoW)
        login_service = LoginService(repoR, repoW)

        users: List[Tuple[str, str, str, str]] = [
            ("taks123", "1Q2w3e4r!@$", "takgyun Lee", "Taks"),
            ("hahahoho119", "1B2n3m4!@", "Ho Han", "Hans"),
            ("mygun7749", "$1Awb5$123", "Guna Yoo", "YoYo"),
        ]
        for id, pw, name, nick in users:
            ret = create_user_service.create(
                account=id,
                passwd=pw,
                name=name,
                nickname=nick,
                auths=[  # Nomal User Auth List
                    Auth(
                        Policy.UserDataReadAblePolicy, TargetScope.Own
                    ),  # 자신의 유저 정보 열람가능
                    Auth(
                        Policy.UserDataDeleteAblePolicy, TargetScope.Own
                    ),  # 자기 계정 삭제가능
                    Auth(
                        Policy.PostReadAblePolicy, TargetScope.Allowed
                    ),  # 공개된 일기 읽기 가능
                    Auth(Policy.PostReadAblePolicy, TargetScope.Own),  # 자기 일기 읽기 가능
                    Auth(Policy.PostDeleteAblePolicy, TargetScope.Own),  # 자기 일기 삭제가능
                    Auth(
                        Policy.PostCreateAndUpdateAblePolicy, TargetScope.Own
                    ),  # 자기 일기 수정가능
                    Auth(Policy.PostPublicAblePolicy, TargetScope.Own),  # 자기 일기 공개가능
                    Auth(Policy.PostPrivateAblePolicy, TargetScope.Own),  # 자기 일기 비공개가능
                ],
            )

        # u = create_user_service.create("taks123", "1Q2w3e4r!@$", "takgyun Lee", "Taks")
        # users.append(u)
        # u = create_user_service.create("hahahoho119", "1B2n3m4!@", "Ho Han", "Hans")
        # users.append(u)
        # u = create_user_service.create("mygun7749", "$1Awb5$123", "Guna Yoo", "YoYo")
        # users.append(u)

        self.create_user_service = create_user_service
        self.login_service = login_service

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        factory = test_selector.get_test_factory("user_service_test_")
        # 썻으면 삭제
        migrate = test_selector.get_usecase_migration(factory)
        if migrate.check_exist_user():
            migrate.delete_user()

        self.assertFalse(migrate.check_exist_user())

    def test_login_user_로그인_안_되는거_확인(self):
        print("\t\t", sys._getframe(0).f_code.co_name)

        user: UserVO = self.login_service.login("tak123", "1Q2w3e4r!@$")

        self.assertDictEqual(
            {"type": "IDNotFound"},
            user.__dict__,
        )

        user = self.login_service.login("hahahoho119", "2N3maa4!@")

        self.assertDictEqual(
            {"type": "PasswardNotCorrect"},
            user.__dict__,
        )

    def test_login_user_잘_로그인_되는거_확인(self):
        print("\t\t", sys._getframe(0).f_code.co_name)

        user = self.login_service.login("taks123", "1Q2w3e4r!@$")
        match user:
            case _user if isinstance(_user, SimpleUser):
                user = _user
            case _:
                self.assertTrue(False)
                return

        self.assertEqual(user.get_account(), "taks123")
        self.assertEqual(user.get_user_nickname(), "Taks")
        self.assertEqual(user.get_uid().idx, 1)
        self.assertEqual(user.auth.auths, self.일반사용자_auths)
        self.assertEqual(user.get_post_num(), 0)

        user = self.login_service.login("hahahoho119", "1B2n3m4!@")
        match user:
            case _user if isinstance(_user, SimpleUser):
                user = _user
            case _:
                self.assertTrue(False)
                return

        self.assertEqual(user.get_account(), "hahahoho119")
        self.assertEqual(user.get_user_nickname(), "Hans")
        self.assertEqual(user.get_uid().idx, 2)
        self.assertEqual(user.auth.auths, self.일반사용자_auths)
        self.assertEqual(user.get_post_num(), 0)

        user = self.login_service.login("mygun7749", "$1Awb5$123")

        match user:
            case _user if isinstance(_user, SimpleUser):
                user = _user
            case _:
                self.assertTrue(False)
                return
        self.assertEqual(user.get_account(), "mygun7749")
        self.assertEqual(user.get_user_nickname(), "YoYo")
        self.assertEqual(user.get_uid().idx, 3)
        self.assertEqual(user.auth.auths, self.일반사용자_auths)
        self.assertEqual(user.get_post_num(), 0)

    def test_result(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        self.assertEqual({"type": "basic"}, Fail(type="basic").__dict__)

        self.assertTrue(issubclass(Fail_CreateUser_IDAlreadyExists, Fail))
        self.assertTrue(isinstance(Fail_CreateUser_IDAlreadyExists(), Fail))
        self.assertEqual(
            {"type": "IDAlreadyExists"}, Fail_CreateUser_IDAlreadyExists().__dict__
        )

        self.assertTrue(issubclass(Fail_CheckUser_IDNotFound, Fail))
        self.assertTrue(isinstance(Fail_CheckUser_IDNotFound(), Fail))
        self.assertEqual({"type": "IDNotFound"}, Fail_CheckUser_IDNotFound().__dict__)

    def test_start_data(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        user = self.login_service.login("taks123", "1Q2w3e4r!@$")
        match user:
            case _user if isinstance(_user, SimpleUser):
                user = _user
            case _:
                self.assertTrue(False)
                return

        self.assertEqual(user.get_account(), "taks123")
        self.assertEqual(user.get_user_nickname(), "Taks")
        self.assertEqual(user.get_uid().idx, 1)
        self.assertEqual(user.auth.auths, self.일반사용자_auths)
        self.assertEqual(user.get_post_num(), 0)

        user = self.login_service.login("hahahoho119", "1B2n3m4!@")
        match user:
            case _user if isinstance(_user, SimpleUser):
                user = _user
            case _:
                self.assertTrue(False)
                return

        self.assertEqual(user.get_account(), "hahahoho119")
        self.assertEqual(user.get_user_nickname(), "Hans")
        self.assertEqual(user.get_uid().idx, 2)
        self.assertEqual(user.auth.auths, self.일반사용자_auths)
        self.assertEqual(user.get_post_num(), 0)

        user = self.login_service.login("mygun7749", "$1Awb5$123")

        match user:
            case _user if isinstance(_user, SimpleUser):
                user = _user
            case _:
                self.assertTrue(False)
                return

        self.assertEqual(user.get_account(), "mygun7749")
        self.assertEqual(user.get_user_nickname(), "YoYo")
        self.assertEqual(user.get_uid().idx, 3)
        self.assertEqual(user.auth.auths, self.일반사용자_auths)
        self.assertEqual(user.get_post_num(), 0)

    def test_중복_아이디_생성하는지_확인(self):
        print("\t\t", sys._getframe(0).f_code.co_name)

        # 중복 아이디
        ret = self.create_user_service.create(
            "taks123", "1Q2w3e4r!@$", "takgyun Lee", "Taks"
        )
        match ret:
            case _ if isinstance(ret, Fail):
                self.assertTrue(True)
            case _:
                print(ret.__dict__)
                self.assertTrue(False)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
