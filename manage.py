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
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default=5000)
    parser.add_argument("--storage_type", default="mysql")
    parser.add_argument(
        "--ver",
        choices=["python", "python3.11"],
        default="python3.11",
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
    from init_data import init_post, init_user

    factory: IStorageFactory = get_strage_factory()

    m: IMigrations = factory.get_migrations()

    delete_storage()
    m.create_user()
    m.create_post()
    try:
        init_user()
        init_post()
    except:
        print("init_data.py를 설정해주세요!")


def set_storage(storage_type: str):
    from Infrastructures.IOC import select_strage

    select_strage(storage_type)


def main(opt):
    from icecream import ic

    debug = opt.debug

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
