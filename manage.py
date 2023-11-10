import __init__

import argparse
import os
import subprocess


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run",
        choices=["test", "git-push", "flask", "migrate", "delete-storage"],
        default="flask",
    )
    parser.add_argument("--branch", default="main")
    parser.add_argument("--not_debug", action="store_false", default=True)
    parser.add_argument("--storage_type", default="mysql")
    parser.add_argument(
        "--test_file",
        nargs="*",
        default=[
            r"Tests\Domains\test_entities.py",
            r"Tests\Applications\Usecases\test_user_services.py",
            r"Tests\Infrastructures\Storage\test_.py",
            r"Tests\Infrastructures\Storage\test_migrate.py",
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
    from Infrastructures.IOC import get_strage_factory
    from Infrastructures.Interfaces import IStorageFactory
    from Applications.Repositories.Interfaces import IUserRepository

    admin = {
        "id": "admin",
        "pw": "admin123",
        "name": "관리자",
    }
    users = [
        admin,
    ]
    create = CreateUser(get_strage_factory().get_user_strage())

    for user in users:
        create.create(user["id"], user["pw"], user["name"])


def migrate():
    from Infrastructures.IOC import get_strage_factory
    from Infrastructures.Interfaces import IStorageFactory, IMigrations
    from Domains.Entities import User, Post

    factory: IStorageFactory = get_strage_factory()

    m: IMigrations = factory.get_migrations()

    m.create_user()
    m.create_post()
    init_user()


def delete_storage():
    from Infrastructures.IOC import get_strage_factory
    from Infrastructures.Interfaces import IStorageFactory, IMigrations

    factory: IStorageFactory = get_strage_factory()

    m: IMigrations = factory.get_migrations()

    m.delete_post()
    m.delete_user()


def set_storage(storage_type: str):
    from Infrastructures.IOC import select_strage

    select_strage(storage_type)


def main(opt):
    print(f"Run {opt.run}")
    set_storage(opt.storage_type)
    match opt.run:
        case "test":
            test(opt.test_file)
        case "git-push":
            git_push(opt.test_file, opt.branch)
        case "flask":
            flask(opt.not_debug)
        case "migrate":
            migrate()
        case "delete-storage":
            delete_storage()
        case _:
            print("'python manage.py -h' 명령어도 인자를 확인해 주세요.")


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
