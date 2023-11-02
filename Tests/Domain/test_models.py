import __init__
import unittest
import sys

from Domains.Models import User, Post
from Commons import UserID, Password, Content


class test_mole(unittest.TestCase):
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
        user = User(UserID(id=1), "takgyun", Password(pw="1qaz2wsx!@"))
        self.assertDictEqual(
            {
                "user_id": UserID(id=1),
                "name": "takgyun",
                "password": Password(pw="1qaz2wsx!@"),
            },
            user.__dict__,
        )

    def test_Post_1(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        post = Post("test", Content(content="test 입니다."), UserID(id=1))
        self.assertDictEqual(
            {
                "title": "test",
                "content": Content(content="test 입니다."),
                "user_id": UserID(id=1),
            },
            post.__dict__,
        )


if __name__ == "__main__":
    unittest.main()
