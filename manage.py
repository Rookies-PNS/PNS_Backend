import __init__

import argparse
import os
import subprocess


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", choices=["test", "git-push", "flask"], default="flask")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--not_debug", action="store_false", default=True)
    parser.add_argument(
        "--test_file",
        nargs="*",
        default=[
            r"Tests\Domains\test_entities.py",
            r"Tests\Applications\Usecase\test_user_services.py",
        ],
    )
    opt = parser.parse_args()
    return opt


def test(test_list: list) -> bool:
    fail = False

    test_exe = "python -m unittest"

    for test in test_list:
        test_py = f"{test_exe} {test}"
        ret = subprocess.call(test_py, shell=True)
        if ret == 1:
            fail = True
    if fail:
        print("==================test가 실패했습니다=========================")

    return not fail


def git_push(test_list: list, branch="main"):
    if test(test_list):
        exe = f"git push origin {branch}"
        subprocess.call(exe, shell=True)


def flask(debug=True):
    from Services.Flask.board_site import app

    app.run(debug=debug)


# def create_table():
#     from get_db_data import get_mysql_url
#     from pathlib import Path
#     import os

#     origin_path = os.getcwd()
#     root_path = Path(__file__).resolve().parent
#     yoyo_dir = r"Infrastructures\Yoyo"
#     yoyo_dir = str(root_path / yoyo_dir)
#     os.chdir(yoyo_dir)

#     try:
#         exe = f"yoyo apply --database {get_mysql_url()} {yoyo_dir}"
#         print(exe)
#         subprocess.call(exe, shell=True)
#     except Exception as ex:
#         print(ex)
#     finally:
#         os.chdir(origin_path)


def main(opt):
    print(f"Run {opt.run}")
    match opt.run:
        case "test":
            test(opt.test_file)
        case "git-push":
            git_push(opt.test_file, opt.branch)
        case "flask":
            flask(opt.not_debug)
        # case "create-table":
        #     create_table()
        case _:
            print("'python manage.py -h' 명령어도 인자를 확인해 주세요.")


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
