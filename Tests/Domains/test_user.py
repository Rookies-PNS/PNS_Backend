import __init__
import unittest
import sys
from datetime import datetime, timedelta

from Domains.Entities import User, SimpleUser, SecuritySimpleUser
from Commons import (
    Uid,
    UserId,
    Password,
    UpdateableTime,
    AuthArchives,
    Auth,
    Policy,
    TargetScope,
    LoginData,
    PostCounter,
)
from icecream import ic


class test_user(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name, f"(test_user)")
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
            Auth(
                Policy.UserAuthLockOfPostCreateAndUpdatePolicy, TargetScope.All
            ),  # 일기 쓰기 권한정지 권한
            Auth(
                Policy.UserAuthUnlockOfPostCreateAndUpdatePolicy, TargetScope.All
            ),  # 일기 쓰기 권한정기 해제 권한
            Auth(Policy.UserDataReadAblePolicy, TargetScope.All),  # 모든 유저 정보 열람가
            Auth(Policy.UserDataDeleteAblePolicy, TargetScope.All),  # 모든 계정 삭제가능
        ]

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

    def test_LoginData_1_lock_time_expired(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        # 잠긴 상태로 설정하고, 잠긴 시간을 현재 시간에서 5분 전으로 설정
        before = datetime.now() - timedelta(minutes=5)
        user = User(
            user_id=UserId("taks123"),
            name="takgyun",
            nickname="일반사용자",
            pw=Password(pw="1qaz2wsx!@"),
            uid=Uid(idx=1),
            auth=AuthArchives(auths=self.일반사용자_auths),
            login_data=LoginData(
                lock_time=UpdateableTime(before),
                lock_flag=True,
                count_of_login_fail=3,
            ),
            post_count=PostCounter(UpdateableTime(before)),
        )
        # 로그인이 가능한 상태 확인 (잠긴 상태가 해제됨)
        self.assertTrue(user.check_login_able())
        self.assertEqual(3, user.get_count_of_login_fail())

        # 로그인 성공
        user.success_login()
        self.assertEqual(0, user.get_count_of_login_fail())

    def test_LoginData_2_lock_time_expired(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        before = datetime.now() - timedelta(minutes=5)
        user = User(
            user_id=UserId("taks123"),
            name="takgyun",
            nickname="일반사용자",
            pw=Password(pw="1qaz2wsx!@"),
            uid=Uid(idx=1),
            auth=AuthArchives(auths=self.일반사용자_auths),
            login_data=LoginData(UpdateableTime(before), True),
            post_count=PostCounter(UpdateableTime(before)),
        )
        # 잠긴 상태로 설정하고, 잠긴 시간을 현재 시간에서 5분 전으로 설정
        # 로그인이 가능한 상태 확인 (잠긴 상태가 해제됨)
        self.assertTrue(user.check_login_able())
        self.assertEqual(0, user.get_count_of_login_fail())
        # 로그인 성공
        user.success_login()

        # lock
        user.lock_login(5)
        self.assertFalse(user.check_login_able())
        self.assertEqual(0, user.get_count_of_login_fail())
        # 로그인 성공
        user.success_login()
        self.assertTrue(user.check_login_able())

    def test_auth_1(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        auths = [
            Auth(Policy.UserDataReadAblePolicy, TargetScope.Own),
            Auth(Policy.PostPrivateAblePolicy, TargetScope.Own),
            Auth(Policy.UserAuthLockOfPostPublicPolicy, TargetScope.Own),
            Auth(Policy.UserAuthUnlockOfPostPublicPolicy, TargetScope.Own),
            Auth(Policy.UserDataReadAblePolicy, TargetScope.Own),
            Auth(Policy.UserDataDeleteAblePolicy, TargetScope.Own),
        ]
        now = datetime.now()
        user = User(
            user_id=UserId("taks123"),
            name="takgyun",
            nickname="일반사용자",
            pw=Password(pw="1qaz2wsx!@"),
            uid=Uid(idx=1),
            auth=AuthArchives(auths=self.공유일기관리자_auths),
            login_data=LoginData(UpdateableTime(now)),
            post_count=PostCounter(UpdateableTime(now)),
        )
        for auth in reversed(auths):
            self.assertTrue(auth.target_range, user.check_policy(auth.policy))

    def test_User_1(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        now = datetime.now()
        user = User(
            user_id=UserId("taks123"),
            name="takgyun",
            nickname="일반사용자",
            pw=Password(pw="1qaz2wsx!@"),
            uid=Uid(idx=1),
            auth=AuthArchives(
                auths=[
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
                ]
            ),
            login_data=LoginData(UpdateableTime(now)),
            post_count=PostCounter(UpdateableTime(now)),
        )
        self.assertEqual("taks123", user.get_account())
        self.assertEqual("takgyun", user.get_user_name())
        self.assertEqual("일반사용자", user.get_user_nickname())
        self.assertEqual("1qaz2wsx!@", user.get_passwd())
        self.assertEqual(Uid(idx=1), user.get_uid())
        for auth in reversed(self.일반사용자_auths):
            self.assertTrue(auth.target_range in user.check_policy(auth.policy))

        self.assertEqual(
            [],
            user.check_policy(
                Auth(
                    Policy.UserAuthUnlockOfPostCreateAndUpdatePolicy,
                    TargetScope.All,
                )
            ),
        )

    def test_count_post_num_same_day(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        now = datetime.now()
        user = User(
            user_id=UserId("taks123"),
            name="takgyun",
            nickname="일반사용자",
            pw=Password(pw="1qaz2wsx!@"),
            uid=Uid(idx=1),
            auth=AuthArchives(auths=self.공유일기관리자_auths),
            login_data=LoginData(UpdateableTime(now)),
            post_count=PostCounter(
                last_update_date=UpdateableTime(datetime.now()),
                post_num=2,
            ),
        )

        # count_post_num 메서드 호출 후 게시물 수 확인
        user.count_post_num()
        self.assertEqual(3, user.get_post_num())

    def test_count_post_num_different_day(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        now = datetime.now()
        user = User(
            user_id=UserId("taks123"),
            name="takgyun",
            nickname="일반사용자",
            pw=Password(pw="1qaz2wsx!@"),
            uid=Uid(idx=1),
            auth=AuthArchives(auths=self.공유일기관리자_auths),
            login_data=LoginData(UpdateableTime(now)),
            post_count=PostCounter(
                last_update_date=UpdateableTime(datetime.now() - timedelta(days=1)),
                post_num=2,
            ),
        )

        # count_post_num 메서드 호출 후 게시물 수 확인
        user.count_post_num()
        self.assertEqual(1, user.get_post_num())

    def test_get_post_num_reset_on_new_day(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        now = datetime.now()
        user = User(
            user_id=UserId("taks123"),
            name="takgyun",
            nickname="일반사용자",
            pw=Password(pw="1qaz2wsx!@"),
            uid=Uid(idx=1),
            auth=AuthArchives(auths=self.공유일기관리자_auths),
            login_data=LoginData(UpdateableTime(now)),
            post_count=PostCounter(
                last_update_date=UpdateableTime(datetime.now() - timedelta(days=1)),
                post_num=2,
            ),
        )

        # get_post_num 메서드 호출 후 게시물 수 확인
        self.assertEqual(0, user.get_post_num())

    def test_simple_user(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        now = datetime.now()
        user = SimpleUser(
            user_id=UserId("taks123"),
            nickname="일반사용자",
            uid=Uid(idx=1),
            auth=AuthArchives(auths=self.공유일기관리자_auths),
            post_count=PostCounter(UpdateableTime(now)),
        )

        now = datetime.now()
        user = SimpleUser(
            user_id=UserId("taks123"),
            nickname="일반사용자",
            uid=Uid(idx=1),
            auth=AuthArchives(auths=self.공유일기관리자_auths),
            post_count=PostCounter(
                last_update_date=UpdateableTime(datetime.now() - timedelta(days=1)),
                post_num=2,
            ),
        )

        # get_post_num 메서드 호출 후 게시물 수 확인
        self.assertEqual(0, user.get_post_num())

        # count_post_num 메서드 호출 후 게시물 수 확인
        user.count_post_num()
        self.assertEqual(1, user.get_post_num())

    def test_security_simple_user(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        # 잠긴 상태로 설정하고, 잠긴 시간을 현재 시간에서 5분 전으로 설정
        before = datetime.now() - timedelta(minutes=5)
        user = SecuritySimpleUser(
            user_id=UserId("taks123"),
            nickname="일반사용자",
            uid=Uid(idx=1),
            auth=AuthArchives(auths=self.일반사용자_auths),
            login_data=LoginData(
                lock_time=UpdateableTime(before),
                lock_flag=True,
                count_of_login_fail=3,
            ),
            post_count=PostCounter(UpdateableTime(before)),
        )
        # 로그인이 가능한 상태 확인 (잠긴 상태가 해제됨)
        self.assertTrue(user.check_login_able())
        self.assertEqual(3, user.get_count_of_login_fail())

        # 로그인 성공
        user.success_login()
        self.assertEqual(0, user.get_count_of_login_fail())
        before = datetime.now() - timedelta(minutes=5)
        user = SecuritySimpleUser(
            user_id=UserId("taks123"),
            nickname="일반사용자",
            uid=Uid(idx=1),
            auth=AuthArchives(auths=self.일반사용자_auths),
            login_data=LoginData(UpdateableTime(before), True),
            post_count=PostCounter(UpdateableTime(before)),
        )
        # 잠긴 상태로 설정하고, 잠긴 시간을 현재 시간에서 5분 전으로 설정
        # 로그인이 가능한 상태 확인 (잠긴 상태가 해제됨)
        self.assertTrue(user.check_login_able())
        self.assertEqual(0, user.get_count_of_login_fail())
        # 로그인 성공
        user.success_login()

        # lock
        user.lock_login(5)
        self.assertFalse(user.check_login_able())
        self.assertEqual(0, user.get_count_of_login_fail())
        # 로그인 성공
        user.success_login()
        self.assertTrue(user.check_login_able())


def main():
    unittest.main()


if __name__ == "__main__":
    main()
