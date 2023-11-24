from Commons.Types.ID import PostId
import __init__
import unittest
import sys
from typing import List
from datetime import datetime, timezone

from Commons import UserId, Uid, Password
from Domains.Entities import UserVO, User, Post, PostVO, SimplePost,SimpleUser
from Applications.Usecases import CreateUser, LoginUser
from Applications.Usecases import (
    CreatePost,
    DeletePost,
    GetPost,
    GetPostList,
    UpdatePost,
)
from Applications.Results import (
    Result,
    Fail,
)

import Tests.Applications.Usecases.storage_selecter as test_selector
from icecream import ic

class test_post_user_services(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name)
        cls.factory = test_selector.get_test_factory("post_user_service_test_")

        migrate = test_selector.get_usecase_migration(cls.factory)
        # 깔끔하게 지우고 시작
        if migrate.check_exist_post():
            migrate.delete_post()

        if migrate.check_exist_user():
            migrate.delete_user()
        # 테이블 생성
        migrate.create_user()

        # 기본세팅
        repo = test_selector.get_user_storage(cls.factory)
        create_user = CreateUser(repo)
        login_user = LoginUser(repo)

        users:List[SimpleUser] = []
        u = create_user.create("taks123", "1Q2w3e4r!@$", "takgyun Lee")
        users.append(u)
        u = create_user.create("hahahoho119", "1B2n3m4!@", "Ho Han")
        users.append(u)
        u = create_user.create("mygun7749", "$1Awb5$123", "Guna Yoo")
        users.append(u)

        cls.origin_users = users
        cls.create_user = CreateUser(repo)
        cls.login_user = LoginUser(repo)

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

        post_repo = test_selector.get_post_storage(self.factory)
        user_repo = test_selector.get_user_storage(self.factory)

        self.get_post_list = GetPostList(post_repo)
        self.create_post = CreatePost(post_repo, user_repo)
        self.get_post = GetPost(post_repo)
        self.update_post = UpdatePost(post_repo, user_repo)
        self.delete_post = DeletePost(post_repo, user_repo)

        post1 = self.create_post.create("Post 1", "Content 1",user = self.origin_users[0])
        post2 = self.create_post.create("Post 2", "Content 2",user = self.origin_users[1])
        post3 = self.create_post.create("Post 3", "Content 3",user = self.origin_users[2])

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        # Delete post table
        migrate = test_selector.get_usecase_migration(self.factory)
        if migrate.check_exist_post():
            migrate.delete_post()
        self.assertFalse(migrate.check_exist_post())

    def test_(self):
        print("\t\t", sys._getframe(0).f_code.co_name)

    def test_(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        now = datetime.now(tz=timezone.utc)
        now = now.replace(microsecond=0)
        user = self.origin_users[0]

        new_post = self.create_post.create("New Post", "New Content", now,user)
        self.assertEqual("New Post", new_post.title)
        self.assertEqual(
            now.strftime("%d/%m/%Y, %H:%M:%S"),
            new_post.create_time.get_time().strftime("%d/%m/%Y, %H:%M:%S"),
        )
        self.assertEqual(
            now.strftime("%d/%m/%Y, %H:%M:%S"),
            new_post.update_time.get_time().strftime("%d/%m/%Y, %H:%M:%S"),
        )

        check_post = self.get_post.get_post_from_post_id(new_post.post_id.idx)
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
        self.assertEqual(
            user.__dict__,
            check_post.user.__dict__
        )

        post_list = self.get_post_list.get_list_no_filter()
        self.assertEqual(len(post_list), 4)

def main():
    unittest.main()


if __name__ == "__main__":
    main()
