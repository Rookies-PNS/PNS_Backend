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
    parser.add_argument("--storage_type", default="mysql")
    parser.add_argument(
        "--test_file",
        nargs="*",
        default=[
            r"Tests\Domains\test_user.py",
            r"Tests\Domains\test_post.py",
            r"Tests\Applications\Usecases\test_user_services.py",
            r"Tests\Infrastructures\Storage\test_.py",
            r"Tests\Infrastructures\Storage\test_migrate.py",
            r"Tests\Applications\Usecases\test_password.py",
            r"Tests\Applications\Usecases\test_contents.py",
            r"Tests\Applications\Usecases\test_post_services.py",
            r"Tests\Applications\Usecases\test_post_user_services.py",
        ],
    )
    opt = parser.parse_args()
    return opt


def test(test_list: list) -> bool:
    fail = False

    test_exe = "python -m unittest"
    fail_list = []

    for test in test_list:
        test_py = f"{test_exe} {test}"
        print("Test", test)
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


def flask(debug=True):
    from Services.Flask.board_site import app

    app.run(debug=debug)


def init_user():
    from Applications.Usecases import CreateUser
    from Domains.Entities.User import SimpleUser
    from Infrastructures.IOC import get_strage_factory
    from Infrastructures.Interfaces import IStorageFactory
    from Applications.Repositories.Interfaces import IUserRepository

    admin = {
        "id": "admin",
        "pw": "Admin123!@",
        "name": "관리자",
    }
    users = [
        admin,
    ]
    create = CreateUser(get_strage_factory().get_user_strage())

    for user in users:
        ret = create.create(user["id"], user["pw"], user["name"])
        match ret:
            case _ if isinstance(ret, SimpleUser):
                ic(ret)
            case _:
                ic("Fail", ret)


def init_post():
    from Applications.Usecases import CreatePost, LoginUser
    from Domains.Entities import SimplePost
    from Infrastructures.IOC import get_post_storage, get_user_storage
    from Infrastructures.Interfaces import IStorageFactory
    from Applications.Repositories.Interfaces import IUserRepository, IPostRepository
    from datetime import datetime, timedelta

    now = datetime.now()
    now = now.replace(microsecond=0)

    login = LoginUser(get_user_storage())
    admin = login.login("admin", "Admin123!@")
    create = CreatePost(get_post_storage(), get_user_storage())

    start = {
        "title": "사이트의 시작을 알립니다.",
        "content": f"""이 사이트는 {now.strftime("%Y/%m/%d")}에 시작했습니다.
이용자 여러분 앞으로 잘 부탁드립니다.""",
        "user": admin,
        "time": now,
    }
    now = now + timedelta(minutes=5)
    anony_post = {
        "title": "여기 짱이 누구냐",
        "content": f"""짜잔! 내가 등장했다!!
이 게시판은 내가 먹도록 하겠다.""",
        "user": None,
        "time": now,
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
            test(opt.test_file)
        case "git-push":
            git_push(opt.test_file, opt.branch)
        case "flask":
            flask(debug)
        case "migrate":
            migrate()
        case "delete-storage":
            delete_storage()
        case _:
            print("'python manage.py -h' 명령어도 인자를 확인해 주세요.")


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
