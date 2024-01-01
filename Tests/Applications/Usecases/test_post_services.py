import __init__
import unittest
import sys
from typing import List, Tuple
from datetime import datetime, timezone

from Commons import *
from Domains.Entities import SimpleUser
from Applications.Usecases.UserServices import CreateUserService, LoginService
from Applications.Usecases.PostServices import (
    CreatePostService,
    DeletePostService,
    GetPublicPostService,
    GetPrivatePostService,
    UpdatePostService,
)
from Applications.Results import (
    Result,
    Fail,
)

import Tests.Applications.Usecases.storage_selecter as test_selector
from icecream import ic


class test_post_services(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name)
        cls.factory = test_selector.get_test_factory("post_service_test_")

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

        migrate = test_selector.get_usecase_migration(cls.factory)
        # 깔끔하게 지우고 시작
        if migrate.check_exist_post():
            migrate.delete_post()

        if migrate.check_exist_user():
            migrate.delete_user()
        # 테이블 생성
        migrate.create_user()

        repoW, repoR = test_selector.get_user_storage(cls.factory)
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

        cls.origin_users = users
        cls.create_user_service = create_user_service
        cls.login_user_service = login_service

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)
        # 썻으면 삭제
        migrate = test_selector.get_usecase_migration(cls.factory)

        if migrate.check_exist_user():
            migrate.delete_user()
        cls.assertFalse(False, migrate.check_exist_user())

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        # Create post table
        migrate = test_selector.get_usecase_migration(self.factory)
        if migrate.check_exist_post():
            migrate.delete_post()
        migrate.create_post()
        self.assertTrue(migrate.check_exist_post())

        post_repoW, post_repoR = test_selector.get_post_storage(self.factory)
        user_repoW, user_repoR = test_selector.get_user_storage(self.factory)

        self.create_post_service = CreatePostService(post_repoW, user_repoW)
        self.get_private_post_service = GetPrivatePostService(post_repoW)
        self.get_public_post_service = GetPublicPostService(post_repoW)
        self.update_post_service = UpdatePostService(post_repoW, user_repoW)
        self.delete_post_service = DeletePostService(post_repoW, user_repoW)

        post1 = self.create_post_service.create(
            "Post 1", "Content 1", self.origin_users[0]
        )
        post2 = self.create_post_service.create(
            "Post 2", "Content 2", self.origin_users[1]
        )
        post3 = self.create_post_service.create(
            "Post 3", "Content 3", self.origin_users[2]
        )

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        # Delete post table
        migrate = test_selector.get_usecase_migration(self.factory)
        if migrate.check_exist_post():
            migrate.delete_post()
        self.assertFalse(migrate.check_exist_post())

    def test_get_post_list(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        post_list = self.get_public_post_service.get_list_no_filter()

        self.assertEqual(len(post_list), 3)

    def test_create_post(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        now = datetime.now(tz=timezone.utc)
        now = now.replace(microsecond=0)

        new_post = self.create_post_service.create(
            "New Post", "New Content", self.origin_users[0], now
        )
        self.assertEqual("New Post", new_post.title)
        self.assertEqual(
            now.strftime("%d/%m/%Y, %H:%M:%S"),
            new_post.create_time.get_time().strftime("%d/%m/%Y, %H:%M:%S"),
        )
        self.assertEqual(
            now.strftime("%d/%m/%Y, %H:%M:%S"),
            new_post.update_time.get_time().strftime("%d/%m/%Y, %H:%M:%S"),
        )

        check_post = self.get_private_post_service.get_post_from_post_id(
            new_post.post_id.idx
        )
        self.assertEqual("New Post", check_post.title)
        self.assertEqual("New Content", check_post.content.content)
        self.assertEqual(
            now.strftime("%d/%m/%Y, %H:%M:%S"),
            check_post.create_time.get_time().strftime("%d/%m/%Y, %H:%M:%S"),
        )
        self.assertEqual(
            now.strftime("%d/%m/%Y, %H:%M:%S"),
            check_post.update_time.get_time().strftime("%d/%m/%Y, %H:%M:%S"),
        )

        post_list = self.get_public_post_service.get_list_no_filter()
        self.assertEqual(len(post_list), 4)

    def test_get_post(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        post = self.get_private_post_service.get_post_from_post_id(1)
        self.assertEqual("Post 1", post.title)
        self.assertEqual("Content 1", post.content.content)

        post_list = self.get_public_post_service.get_list_no_filter()
        self.assertEqual(len(post_list), 3)

    def test_update_post(self):
        import time

        time.sleep(1)
        print("\t\t", sys._getframe(0).f_code.co_name)
        post = self.get_private_post_service.get_post_from_post_id(1)

        updated_post = self.update_post_service.update(
            post, "Updated Post", "Updated Content", self.origin_users[0]
        )
        self.assertEqual(updated_post.title, "Updated Post")
        self.assertEqual(
            post.create_time.get_time(), updated_post.create_time.get_time()
        )
        self.assertNotEqual(
            post.update_time.get_time(), updated_post.update_time.get_time()
        )
        self.assertTrue(
            (
                post.update_time.get_time() - updated_post.update_time.get_time()
            ).total_seconds()
            < 0
        )

        post_list = self.get_public_post_service.get_list_no_filter()
        self.assertEqual(len(post_list), 3)

        check_post = self.get_private_post_service.get_post_from_post_id(
            updated_post.post_id.idx
        )
        self.assertEqual(check_post.title, "Updated Post")
        self.assertEqual(check_post.content.content, "Updated Content")

    def test_delete_post(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        post = self.get_private_post_service.get_post_from_post_id(1)
        self.delete_post_service.delete(post, self.origin_users[0])
        deleted_post = self.get_private_post_service.get_post_from_post_id(1)
        self.assertIsNone(deleted_post)

        post_list = self.get_public_post_service.get_list_no_filter()
        self.assertEqual(len(post_list), 2)

    def test_(self):
        print("\t\t", sys._getframe(0).f_code.co_name)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
