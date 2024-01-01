def init_user():
    from Commons import Auth, Policy, TargetScope
    from Applications.Usecases.UserServices import CreateUserService
    from Domains.Entities.User import SimpleUser
    from Infrastructures.IOC import get_strage_factory
    from Infrastructures.Interfaces import IStorageFactory
    from Applications.Repositories.Interfaces import IUserWriteableRepository
    from icecream import ic

    user_admin = {
        "id": "UserAdmin",
        "pw": "Admin123!@",
        "name": "UserAdmin",
        "nick": "user_admini",
        "auth": [
            Auth(Policy.PostReadAblePolicy, TargetScope.Allowed),  # 공개된 일기 읽기 가능
            Auth(Policy.UserDataReadAblePolicy, TargetScope.Own),  # 자신의 유저 정보 열람가능
            Auth(Policy.PostDeleteAblePolicy, TargetScope.All),  # All 일기 삭제가능
            Auth(
                Policy.UserAuthLockOfPostCreateAndUpdatePolicy, TargetScope.All
            ),  # 일기 쓰기 권한정지 권한
            Auth(
                Policy.UserAuthUnlockOfPostCreateAndUpdatePolicy, TargetScope.All
            ),  # 일기 쓰기 권한정기 해제 권한
            Auth(Policy.UserDataReadAblePolicy, TargetScope.All),  # 모든 유저 정보 열람가능
            Auth(Policy.UserDataDeleteAblePolicy, TargetScope.All),  # 모든 계정 삭제가능
        ],
    }
    post_admin = {
        "id": "PostAdmin",
        "pw": "Admin123!@",
        "name": "PostAdmin",
        "nick": "post_admini",
        "auth": [
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
        ],
    }
    nomal_user = {
        "id": "nomal_id",
        "pw": "1qaz2wsx!@QW",
        "name": "nomaluser",
        "nick": "nomals",
        "auth": [
            Auth(Policy.UserDataReadAblePolicy, TargetScope.Own),  # 자신의 유저 정보 열람가능
            Auth(Policy.UserDataDeleteAblePolicy, TargetScope.Own),  # 자기 계정 삭제가능
            Auth(Policy.PostReadAblePolicy, TargetScope.Allowed),  # 공개된 일기 읽기 가능
            Auth(Policy.PostReadAblePolicy, TargetScope.Own),  # 자기 일기 읽기 가능
            Auth(Policy.PostDeleteAblePolicy, TargetScope.Own),  # 자기 일기 삭제가능
            Auth(Policy.PostCreateAndUpdateAblePolicy, TargetScope.Own),  # 자기 일기 수정가능
            Auth(Policy.PostPublicAblePolicy, TargetScope.Own),  # 자기 일기 공개가능
            Auth(Policy.PostPrivateAblePolicy, TargetScope.Own),  # 자기 일기 비공개가능
        ],
    }
    nomal_user2 = {
        "id": "nomal_id2",
        "pw": "1qaz2wsx!@QW",
        "name": "nomal user",
        "nick": "동네선배",
        "auth": [
            Auth(Policy.UserDataReadAblePolicy, TargetScope.Own),  # 자신의 유저 정보 열람가능
            Auth(Policy.UserDataDeleteAblePolicy, TargetScope.Own),  # 자기 계정 삭제가능
            Auth(Policy.PostReadAblePolicy, TargetScope.Allowed),  # 공개된 일기 읽기 가능
            Auth(Policy.PostReadAblePolicy, TargetScope.Own),  # 자기 일기 읽기 가능
            Auth(Policy.PostDeleteAblePolicy, TargetScope.Own),  # 자기 일기 삭제가능
            Auth(Policy.PostCreateAndUpdateAblePolicy, TargetScope.Own),  # 자기 일기 수정가능
            Auth(Policy.PostPublicAblePolicy, TargetScope.Own),  # 자기 일기 공개가능
            Auth(Policy.PostPrivateAblePolicy, TargetScope.Own),  # 자기 일기 비공개가능
        ],
    }
    users = [
        user_admin,
        post_admin,
        nomal_user,
        nomal_user2,
    ]
    service = CreateUserService(get_strage_factory().get_user_write_storage())

    for user in users:
        ret = service.create(
            account=user["id"],
            passwd=user["pw"],
            name=user["name"],
            nickname=user["nick"],
            auths=user["auth"],
        )
        match ret:
            case none if none is None:
                ic("Succuss")
            case _:
                ic("Fail", ret)


def init_post():
    from Applications.Usecases.UserServices import LoginService
    from Applications.Usecases.PostServices import CreatePostService
    from Domains.Entities import SimplePost
    from Infrastructures.IOC import get_post_storage, get_user_storage
    from Infrastructures.Interfaces import IStorageFactory
    from Applications.Repositories.Interfaces import (
        IUserWriteableRepository,
        IPostWriteableRepository,
    )
    from datetime import datetime, timedelta

    now = datetime.now()
    now = now.replace(microsecond=0)

    (repoW, repoR) = get_user_storage()
    login = LoginService(repoR, repoW)
    nomal = login.login("nomal_id", "1qaz2wsx!@QW")
    nomal2 = login.login("nomal_id2", "1qaz2wsx!@QW")
    create = CreatePostService(get_post_storage()[0], repoW)

    start = {
        "title": "사이트의 시작을 알립니다.",
        "content": f"""이 사이트는 {now.strftime("%Y/%m/%d")}에 시작했습니다.
이용자 여러분 앞으로 잘 부탁드립니다.""",
        "user": nomal,
        "time": now,
        "flag": False,
    }
    now = now + timedelta(minutes=5)
    anony_post = {
        "title": "여기 짱이 누구냐",
        "content": f"""짜잔! 내가 등장했다!!
이 게시판은 내가 먹도록 하겠다.""",
        "user": nomal2,
        "time": now,
        "flag": True,
    }

    posts = [
        start,
        anony_post,
    ]
    for post in posts:
        create.create(
            title=post["title"],
            content=post["content"],
            create_time=post["time"],
            user=post["user"],
            share_flag=False,
            target_time=datetime.now(),
            img=None,
        )
