import __init__

import argparse
import os
import subprocess
from icecream import ic


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run",
        choices=["test", "git-push", "flask", "migrate", "delete-storage"],
        default="flask",
    )
    parser.add_argument("--branch", default="main")
    parser.add_argument("--not_debug", action="store_true", default=False)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=5000)
    parser.add_argument("--storage_type", default="mysql")
    parser.add_argument(
        "--ver",
        choices=["python", "python3.11"],
        default="python",
    )
    parser.add_argument(
        "--test_file",
        nargs="*",
        default=[
            r"Tests/Domains/test_auth.py",
            r"Tests/Domains/test_user.py",
            r"Tests/Domains/test_post.py",
            r"Tests/Applications/Usecases/test_user_services.py",
            r"Tests/Infrastructures/Storage/test_.py",
            r"Tests/Infrastructures/Storage/test_migrate.py",
            r"Tests/Applications/Usecases/test_password.py",
            r"Tests/Applications/Usecases/test_contents.py",
            r"Tests/Applications/Usecases/test_post_services.py",
            r"Tests/Applications/Usecases/test_post_user_services.py",
        ],
    )
    opt = parser.parse_args()
    return opt


def test(test_list: list, py_v="python") -> bool:
    fail = False

    test_exe = f"{py_v} -m unittest"
    fail_list = []

    for test in test_list:
        test_py = f"{test_exe} {test}"
        print(test_exe, test)
        ret = subprocess.call(test_py, shell=True)
        if ret == 1:
            fail_list.append(test)
            fail = True
    if fail:
        print("=======================Fail Test=============================")
        for test in fail_list:
            print(f"\t> {test}")
        print("=======================+++++++++=============================")

    return not fail


def git_push(test_list: list, branch="main"):
    if test(test_list):
        exe = f"git push origin {branch}"
        subprocess.call(exe, shell=True)


def flask(debug=True, host="127.0.0.1", port=5000):
    from Services.Flask.board_site import app

    app.run(debug=debug, host=host, port=int(port))


def init_user():
    from Commons import Auth, Policy, TargetScope
    from Applications.Usecases.UserServices import CreateUserService
    from Domains.Entities.User import SimpleUser
    from Infrastructures.IOC import get_strage_factory
    from Infrastructures.Interfaces import IStorageFactory
    from Applications.Repositories.Interfaces import IUserWriteableRepository

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


def delete_storage():
    from Infrastructures.IOC import get_strage_factory
    from Infrastructures.Interfaces import IStorageFactory, IMigrations

    factory: IStorageFactory = get_strage_factory()

    m: IMigrations = factory.get_migrations()

    if m.check_exist_post():
        m.delete_post()
    if m.check_exist_user():
        m.delete_user()


def migrate():
    from Infrastructures.IOC import get_strage_factory
    from Infrastructures.Interfaces import IStorageFactory, IMigrations
    from Domains.Entities import User, Post

    factory: IStorageFactory = get_strage_factory()

    m: IMigrations = factory.get_migrations()

    delete_storage()
    m.create_user()
    m.create_post()
    init_user()
    init_post()


def set_storage(storage_type: str):
    from Infrastructures.IOC import select_strage

    select_strage(storage_type)


def main(opt):
    from icecream import ic

    debug = not opt.not_debug

    if debug:
        ic.enable()
    else:
        ic.disable()

    print(f"Run {opt.run}")
    set_storage(opt.storage_type)
    match opt.run:
        case "test":
            ic.enable()
            test(opt.test_file, opt.ver)
        case "git-push":
            git_push(opt.test_file, opt.branch)
        case "flask":
            flask(debug, opt.host, opt.port)
        case "migrate":
            migrate()
        case "delete-storage":
            delete_storage()
        case _:
            print("'python manage.py -h' 명령어도 인자를 확인해 주세요.")


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
