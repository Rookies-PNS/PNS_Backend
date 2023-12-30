import __init__
import unittest
import sys
from datetime import datetime, timedelta

from Domains.Entities import PostVO, Post, UserVO
from Commons import (
    Uid,
    UserId,
    PostId,
    Password,
    Content,
    ImageKey,
    SelectTime,
    TimeVO,
    UpdateableTime,
    AuthArchives,
    LoginData,
    PostCounter,
    Auth,
    TargetScope,
    Policy,
)
from icecream import ic


class test_models(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"

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
        print(sys._getframe(0).f_code.co_name, f"(test_post)")

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        self.user = UserVO(
            user_account=UserId("taks123"),
            name="takgyun",
            nickname="일반사용자",
            uid=Uid(idx=1),
            auth=AuthArchives(auths=self.공유일기관리자_auths),
            login_data=LoginData(UpdateableTime(datetime.now())),
            post_count=PostCounter(
                last_update_date=UpdateableTime(datetime.now() - timedelta(days=1)),
                post_num=2,
            ),
        )

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)

    def test_time(self):
        import time

        print("\t\t", sys._getframe(0).f_code.co_name)
        now = datetime.now()
        target_time = SelectTime(now)
        create_time = TimeVO(now)
        update_time = UpdateableTime(now)
        self.assertEqual(
            now.strftime("%Y-%m-%d $ %H:%M"),
            target_time.get_time().strftime("%Y-%m-%d $ %H:%M"),
        )
        self.assertEqual(
            now.strftime("%Y-%m-%d $ %H:%M"),
            create_time.get_time().strftime("%Y-%m-%d $ %H:%M"),
        )
        self.assertEqual(
            now.strftime("%Y-%m-%d $ %H:%M"),
            update_time.get_time().strftime("%Y-%m-%d $ %H:%M"),
        )
        self.assertTrue(target_time.compare_time(now + timedelta(minutes=3)))

        time.sleep(1)
        update_time.set_now()
        self.assertEqual(
            datetime.now().strftime("%Y-%m-%d $ %H:%M:%S"),
            update_time.get_time().strftime("%Y-%m-%d $ %H:%M:%S"),
        )
        self.assertNotEqual(
            target_time.get_time().strftime("%Y-%m-%d $ %H:%M:%S"),
            update_time.get_time().strftime("%Y-%m-%d $ %H:%M:%S"),
        )

        target_time.set_time(update_time.get_time())
        self.assertEqual(
            target_time.get_time().strftime("%Y-%m-%d $ %H:%M:%S"),
            update_time.get_time().strftime("%Y-%m-%d $ %H:%M:%S"),
        )

    def test_Post_1(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        now = datetime.now()
        post = Post(
            title="test",
            content=Content(content="test 입니다."),
            owner=self.user.get_simple_user(),
            target_time=SelectTime(now),
            create_time=TimeVO(now),
            update_time=UpdateableTime(now),
        )

        self.assertEqual("test", post.get_title())
        self.assertEqual(None, post.get_post_id())
        self.assertEqual("Uid(idx=1)", str(post.get_uid()))
        self.assertEqual(
            now.strftime("%Y-%m-%d"),
            str(post.target_time.get_time().strftime("%Y-%m-%d")),
        )
        self.assertEqual("test 입니다.", post.get_content())
        self.assertEqual(
            now.strftime("%Y-%m-%d"),
            str(post.create_time.get_time().strftime("%Y-%m-%d")),
        )
        self.assertEqual(
            now.strftime("%Y-%m-%d"),
            str(post.update_time.get_time().strftime("%Y-%m-%d")),
        )
        self.assertEqual(False, post.share_flag)
        self.assertEqual(None, post.img_key)

    def test_Post_2(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        now = datetime.now()
        post = PostVO(
            title="test",
            content=Content(content="test 입니다."),
            owner=self.user.get_simple_user(),
            target_time=SelectTime(now),
            create_time=TimeVO(now),
            update_time=UpdateableTime(now),
            post_id=PostId(idx=1),
            share_flag=True,
            img_key=ImageKey("my-key"),
        )

        self.assertEqual("test", post.get_title())
        self.assertEqual("PostId(idx=1)", str(post.get_post_id()))
        self.assertEqual("Uid(idx=1)", str(post.get_uid()))
        self.assertEqual(
            now.strftime("%Y-%m-%d"),
            str(post.target_time.get_time().strftime("%Y-%m-%d")),
        )
        self.assertEqual("test 입니다.", post.get_content())
        self.assertEqual(
            now.strftime("%Y-%m-%d"),
            str(post.create_time.get_time().strftime("%Y-%m-%d")),
        )
        self.assertEqual(
            now.strftime("%Y-%m-%d"),
            str(post.update_time.get_time().strftime("%Y-%m-%d")),
        )
        self.assertEqual(True, post.share_flag)
        self.assertEqual("my-key", post.img_key.access_key)
        post = post.get_simple_post()
        self.assertEqual("test", post.get_title())
        self.assertEqual("PostId(idx=1)", str(post.get_post_id()))
        self.assertEqual("Uid(idx=1)", str(post.get_uid()))
        self.assertEqual(
            now.strftime("%Y-%m-%d"),
            str(post.target_time.get_time().strftime("%Y-%m-%d")),
        )
        self.assertEqual(True, post.share_flag)
        self.assertEqual("my-key", post.img_key.access_key)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
