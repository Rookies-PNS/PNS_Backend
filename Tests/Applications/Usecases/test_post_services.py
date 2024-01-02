import __init__
import unittest
import sys
from typing import List, Tuple
from datetime import datetime, timezone

from Commons import *
from Domains.Entities import SimpleUser, SimplePost, PostVO
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
        cls.start_time = datetime.now()
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
            ("taks123", "1Q2w3e4r!@", "takgyun Lee", "Taks"),
            ("hahahoho119", "1B2n3m4!@", "Ho Han", "Hans"),
            ("mygun7749", "$1Awb5$123", "Guna Yoo", "YoYo"),
        ]
        origin_users: List[SimpleUser] = []
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

            match login_service.login(id, pw):
                case user if isinstance(user, SimpleUser):
                    origin_users.append(user)
                case a:
                    raise ValueError()

        cls.origin_users = origin_users
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

        (post_repoW, post_repoR) = test_selector.get_post_storage(self.factory)
        (user_repoW, user_repoR) = test_selector.get_user_storage(self.factory)

        self.create_post_service = CreatePostService(post_repoW, user_repoW)
        self.get_private_post_service = GetPrivatePostService(post_repoR)
        self.get_public_post_service = GetPublicPostService(post_repoR)
        self.update_post_service = UpdatePostService(post_repoW, user_repoW)
        self.delete_post_service = DeletePostService(post_repoW, post_repoR, user_repoW)

        post1 = self.create_post_service.create(
            title="Post 1",
            content="Content 1",
            user=self.origin_users[0],
            share_flag=True,
            target_time=self.start_time,
            img=None,
        )
        post2 = self.create_post_service.create(
            title="Post 2",
            content="Content 2",
            user=self.origin_users[1],
            share_flag=True,
            target_time=self.start_time,
            img=None,
        )
        post3 = self.create_post_service.create(
            title="Post 3",
            content="Content 3",
            user=self.origin_users[2],
            share_flag=False,
            target_time=self.start_time,
            img=None,
        )

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        # Delete post table
        migrate = test_selector.get_usecase_migration(self.factory)
        if migrate.check_exist_post():
            migrate.delete_post()
        self.assertFalse(migrate.check_exist_post())

    def test_get_public_post(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        user = self.origin_users[0]
        post_list = self.get_public_post_service.get_post_list(user)

        post: SimplePost = post_list[0]
        self.assertEqual(1, post.get_post_id().idx)
        self.assertEqual("Post 1", post.get_title())
        self.assertEqual("Taks", post.get_owner_nickname())
        self.assertEqual(True, post.share_flag)

        post: SimplePost = post_list[1]
        self.assertEqual(2, post.get_post_id().idx)
        self.assertEqual("Post 2", post.get_title())
        self.assertEqual("Hans", post.get_owner_nickname())
        self.assertEqual(True, post.share_flag)

        # 공개 일기 조회

        match self.get_public_post_service.get_post_detail(user, 2):
            case ret if isinstance(ret, PostVO):
                post = ret
            case fail:
                ic(fail)
                raise ValueError()

        self.assertEqual("Post 2", post.get_title())
        self.assertEqual("Content 2", post.get_content())

        # 비공개 일기 조회

        self.assertIsInstance(
            self.get_public_post_service.get_post_detail(user, 3), Fail
        )

    def test_create_post(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        now = datetime.now(tz=timezone.utc)
        now = now.replace(microsecond=0)
        user = self.origin_users[0]

        match self.create_post_service.create(
            title="New Post",
            content="New Content",
            user=user,
            share_flag=False,
            target_time=now,
            create_time=now,
            img=None,
        ):
            case none if none is None:
                match self.get_private_post_service.get_post_list(
                    actor=user, page=0, posts_per_page=10
                ):
                    case _list if isinstance(_list, list):
                        new_post = _list[-1]
                    case _:
                        raise ValueError()
            case a:
                self.assertFalse(a)

        self.assertEqual("New Post", new_post.get_title())

        self.assertEqual(
            now.strftime("%d/%m/%Y, %H:%M:%S"),
            new_post.target_time.get_time().strftime("%d/%m/%Y, %H:%M:%S"),
        )

        match self.get_private_post_service.get_post_detail(
            user, new_post.get_post_id().idx
        ):
            case post if isinstance(post, PostVO):
                check_post = post
            case fail:
                ic(fail)
                raise ValueError
        self.assertEqual("New Post", check_post.get_title())
        self.assertEqual("New Content", check_post.get_content())
        self.assertEqual(
            now.strftime("%d/%m/%Y, %H:%M:%S"),
            check_post.target_time.get_time().strftime("%d/%m/%Y, %H:%M:%S"),
        )

        post_list = self.get_private_post_service.get_post_list(user)
        self.assertEqual(len(post_list), 2)

    def test_get_private_post(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        post_list = self.get_public_post_service.get_post_list()

        post = self.get_private_post_service.get_post_detail(1)
        post = self.get_private_post_service.get_post_detail(1)
        self.assertEqual("Post 1", post.title)
        self.assertEqual("Content 1", post.content.content)

        post_list = self.get_public_post_service.get_post_list()
        self.assertEqual(len(post_list), 3)

    def test_update_post(self):
        import time

        time.sleep(1)
        print("\t\t", sys._getframe(0).f_code.co_name)
        post = self.get_private_post_service.get_post_detail(1)

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

        post_list = self.get_public_post_service.get_post_list()
        self.assertEqual(len(post_list), 3)

        check_post = self.get_private_post_service.get_post_detail(
            updated_post.post_id.idx
        )
        self.assertEqual(check_post.title, "Updated Post")
        self.assertEqual(check_post.content.content, "Updated Content")

    def test_delete_post(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        user = self.origin_users[0]
        post_list = self.get_public_post_service.get_post_list(user)
        self.assertEqual(len(post_list), 2)

        post = self.get_private_post_service.get_post_detail(user, 1)

        self.assertIsNone(self.delete_post_service.delete(self.origin_users[0], 1))
        deleted_post = self.get_private_post_service.get_post_detail(user, 1)
        deleted_post = self.get_private_post_service.get_post_detail(user, 1)
        self.assertIsInstance(deleted_post, Fail)

        post_list = self.get_public_post_service.get_post_list(user)
        self.assertEqual(len(post_list), 1)

    def test_(self):
        print("\t\t", sys._getframe(0).f_code.co_name)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
