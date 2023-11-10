import __init__
import unittest
import sys

from Domains.Entities import User, Post
from Commons import Uid, UserId, PostId, Password, Content


class test_(unittest.TestCase):
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

    def test_(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        self.assertTrue(False)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
