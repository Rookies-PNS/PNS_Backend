import __init__
import unittest
import sys
from datetime import datetime, timedelta

from Domains.Entities import SimpleUser
from Applications.Usecases.SessionServices import *
from Applications.Usecases import CreateUser, LoginUser
import Tests.Applications.Usecases.storage_selecter as test_selector
from Tests.Applications.Implements.test_session_repository_list import (
    TestSessionRepository,
)


class TestSessionManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name)

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)

    @classmethod
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        Sfactory = test_selector.get_session_storage("session_service_test_")
        factory = test_selector.get_test_factory("user_service_test_")

        self.create_session = PublichSessionService(Sfactory, factory)
        self.verify_session = VerifySession(Sfactory)
        user = SimpleUser(user_id="test_user")

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        factory = test_selector.get_test_factory("user_service_test_")

        migrate = test_selector.get_usecase_migration(factory)
        if migrate.check_exist_user():
            migrate.delete_user()

        self.assertFalse(migrate.check_exist_user())

    def session_세션_생성확인(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        self.new = TestSessionRepository.publish_Session
        new = self.new
        print(new)
        match new:
            case _ if isinstance(new, Fail):
                self.assertTrue(False)
            case _:
                pass


if __name__ == "__main__":
    unittest.main()
