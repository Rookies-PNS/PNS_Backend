import __init__
import json


def get_secrets_file() -> str:
    import os, sys

    path = "secrets.json"
    for root in reversed(sys.path):
        join_path = os.path.join(root, path)
        if os.path.isfile(join_path):
            return os.path.abspath(join_path)

    raise FileNotFoundError()


def get_secrets_key() -> str:
    try:
        secret_file = get_secrets_file()  # secrets.json 파일 위치
    except Exception as ex:
        raise ex
    try:
        with open(secret_file) as f:
            secrets = json.loads(f.read())
    except Exception as ex:
        raise ex

    return secrets["SECRET_KEY"]
