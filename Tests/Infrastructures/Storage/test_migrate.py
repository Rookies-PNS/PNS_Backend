import __init__
import unittest  # import IsolatedAsyncioTestCase
import sys
from icecream import ic

import Tests.Infrastructures.Storage.storage_selecter as test_selector


class test_migrate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name)
        ## 썼으면 삭제
        migrate = test_selector.get_storage_migration()
        if migrate.check_exist_img_data():
            migrate.delete_img_data()
        if migrate.check_exist_post():
            migrate.delete_post()
        if migrate.check_exist_user():
            migrate.delete_user()

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        migrate = test_selector.get_storage_migration()
        self.migrate = migrate
        ## 테이블이 없는지 확인
        self.assertFalse(migrate.check_exist_user())
        self.assertFalse(migrate.check_exist_post())
        self.assertFalse(migrate.check_exist_img_data())

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        ## 썼으면 삭제
        if self.migrate.check_exist_img_data():
            self.migrate.delete_img_data()
        if self.migrate.check_exist_post():
            self.migrate.delete_post()
        if self.migrate.check_exist_user():
            self.migrate.delete_user()

        self.assertFalse(self.migrate.check_exist_user())
        self.assertFalse(self.migrate.check_exist_post())

    def test_create_user(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        self.migrate.create_user()
        self.assertTrue(self.migrate.check_exist_user())

    def test_create_post(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        self.migrate.create_user()
        self.migrate.create_post()
        self.assertTrue(self.migrate.check_exist_post())

    def test_create_img_data(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t\t", sys._getframe(0).f_code.co_name)
        self.migrate.create_user()
        self.migrate.create_post()
        self.migrate.create_img_data()
        self.assertTrue(self.migrate.check_exist_img_data())


def main():
    unittest.main()


if __name__ == "__main__":
    main()
