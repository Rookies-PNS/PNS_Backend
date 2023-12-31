import __init__
import unittest
import sys
from icecream import ic
from Applications.Usecases.UserServices.UsecaseUserExtention import (
    validate_account,
    validate_name,
    validate_nickname,
)


class test_user_services(unittest.TestCase):
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

    def test_valid_input_of_CreateUser(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        valid_nickname_with_space = "닉네임 테스트"
        valid_nickname_without_space = "Nick!Name"
        invalid_nickname = " Nick!Name"  # 처음에 띄어쓰기가 포함되어 있음
        too_short_nickname = ""  # 5자 미만
        too_long_nickname = "VeryLongNicknameThatExceedsTheLimit123123123"  # 20자 초과

        self.assertTrue(validate_nickname(valid_nickname_with_space))  # True
        self.assertTrue(validate_nickname(valid_nickname_without_space))  # True
        self.assertFalse(validate_nickname(invalid_nickname))  # False
        self.assertFalse(validate_nickname(too_short_nickname))  # True
        self.assertFalse(validate_nickname(too_long_nickname))  # False

        valid_name_with_space = "홍 길 동"
        valid_name_without_space = "John Doe"
        invalid_name = " John Doe"  # 처음에 띄어쓰기가 포함되어 있음
        too_short_name = "A"  # 2자 미만
        too_long_name = "VeryLongNameThatExceedsTheLimit1"  # 20자 초과

        self.assertFalse(validate_name(valid_name_with_space))  # True
        self.assertTrue(validate_name(valid_name_without_space))  # True
        self.assertFalse(validate_name(invalid_name))  # False
        self.assertFalse(validate_name(too_short_name))  # False
        self.assertFalse(validate_name(too_long_name))  # False

    def test_(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
