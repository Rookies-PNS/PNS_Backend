import __init__
import unittest
import sys
import datetime

from Domains.Entities import User, Post
from Commons import (
    Uid,
    UserId,
    PostId,
    Password,
    Content,
    PostCreateTime,
    PostUpdateTime,
)


class test_models(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name)

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

    def test_User_1(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        user = User(UserId("taks123"), "takgyun", Password(pw="1qaz2wsx!@"), Uid(idx=1))
        self.assertDictEqual(
            {
                "user_id": UserId(account="taks123"),
                "name": "takgyun",
                "password": Password(pw="1qaz2wsx!@"),
                "uid": Uid(idx=1),
            },
            user.__dict__,
        )

    def test_Post_1(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        post = Post("test", Content(content="test 입니다."))

        self.assertDictEqual(
            {
                "title": "test",
                "content": Content(content="test 입니다."),
                "create_time": PostCreateTime(time=post.create_time.get_time()),
                "update_time": PostUpdateTime(time=post.update_time.get_time()),
                "post_id": None,
                "user": None,
            },
            post.__dict__,
        )


def main():
    unittest.main()


if __name__ == "__main__":
    main()
