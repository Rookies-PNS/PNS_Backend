import __init__
import unittest
import sys
from datetime import datetime, timedelta

from Domains.Entities import SimpleUser
from Applications.Usecases.SessionServices import *
from Applications.Usecases import CreateUser, LoginUser
from Tests.Applications.Implements.test_session_repository_list import (
    TestSessionRepository,
)
import Tests.Applications.Usecases.storage_selecter as test_selector


class test_session_services(unittest.TestCase):
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
        factory = test_selector.get_test_factory("user_service_test_")

        migrate = test_selector.get_usecase_migration(factory)
        # 깔끔하게 지우고 시작
        if migrate.check_exist_user():
            migrate.delete_user()
        # 테이블 생성
        migrate.create_user()

        # 기본세팅
        repo = test_selector.get_user_storage(factory)
        create_user = CreateUser(repo)
        login_user = LoginUser(repo)
        session = PublichSessionService
        users = []
        u = create_user.create("taks123", "1Q2w3e4r!@$", "takgyun Lee")
        users.append(u)
        u = create_user.create("hahahoho119", "1B2n3m4!@", "Ho Han")
        users.append(u)
        u = create_user.create("mygun7749", "$1Awb5$123", "Guna Yoo")
        users.append(u)

        self.create_user = CreateUser(repo)
        self.login_user = LoginUser(repo)
        self.session = PublichSessionService

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        factory = test_selector.get_test_factory("user_service_test_")
        # 썻으면 삭제
        migrate = test_selector.get_usecase_migration(factory)
        if migrate.check_exist_user():
            migrate.delete_user()

        self.assertFalse(migrate.check_exist_user())

    def test_login_user_잘_로그인_되는거_확인(self):
        print("\t\t", sys._getframe(0).f_code.co_name)

        user = self.login_user.login("taks123", "1Q2w3e4r!@$")
        match user:
            case _ if isinstance(user, Fail):
                self.assertTrue(False)
            case _:
                pass

    def session_세션_생성확인(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        self.new = TestSessionRepository.publish_Session
        new = self.new
        match new:
            case _ if isinstance(new, Fail):
                self.assertTrue(False)
            case _:
                pass
