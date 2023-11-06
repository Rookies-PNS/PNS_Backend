import __init__
import unittest
import sys
from typing import List

from Commons import UserId, Uid, Password
from Domains.Models import UserVO, User
from Applications.Usecases import CreateUser

from Tests.Applications.Implements.test_user_repository_list import (
    TestUserRepositoryList,
)


class test_create_user(unittest.TestCase):
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
        self.arr: List[UserVO] = []
        self.create_user = CreateUser(TestUserRepositoryList(self.arr))
        self.create_user.create("taks123", "1q2w3e4r!@#$", "takgyun Lee")
        self.create_user.create("hahahoho119", "1b2n3m4!#@", "Ho Han")
        self.create_user.create("mygun7749", "$1#awb5$", "Guna Yoo")

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)

    def test_start_data(self):
        print("\t\t", sys._getframe(0).f_code.co_name)

        user = self.arr[0]

        self.assertDictEqual(
            {
                "user_id": UserId(id="taks123"),
                "name": "takgyun Lee",
                "password": Password(pw="1q2w3e4r!@#$"),
                "uid": Uid(idx=1),
            },
            user.__dict__,
        )

        user = self.arr[1]

        self.assertDictEqual(
            {
                "user_id": UserId(id="hahahoho119"),
                "name": "Ho Han",
                "password": Password(pw="1b2n3m4!#@"),
                "uid": Uid(idx=2),
            },
            user.__dict__,
        )

        user = self.arr[2]

        self.assertDictEqual(
            {
                "user_id": UserId(id="mygun7749"),
                "name": "Guna Yoo",
                "password": Password(pw="$1#awb5$"),
                "uid": Uid(idx=3),
            },
            user.__dict__,
        )


if __name__ == "__main__":
    unittest.main()
