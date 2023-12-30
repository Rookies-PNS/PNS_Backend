import __init__
from typing import Optional, Callable, Final
from Commons import Password

account_len: Final = 10
name_len: Final = 15
nickname_len: Final = 10


def check_valid_password(input_pw: str) -> bool:
    import re

    pattern = re.compile(
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )

    if pattern.match(input_pw):
        return True
    else:
        return False


def get_padding_adder(account: str, nickname: str) -> Callable[[str], str]:
    """_summary_
    특별한 솔트 페퍼를 추가하는 함수를 만들어 주는 함수

    Args:
        account (str): 사용자 고유의 계정
        nickname (str): 사용자 고유의 닉네임

    Returns:
        Callable[[str], str]: funtion(passwd) -> padding_str, 솔트 패퍼해주는 함수를 반환한다.
    """
    before = f"!$&*%?S@1t{account}{nickname}6"
    after = f"9{nickname}{account}P3pp3r?%*&$!"

    def adder(pw: str) -> str:
        return f"{before}{pw}{after}"

    return adder


def convert_to_Password_with_hashing(
    password: str,
    add_sult_pepper: Callable[[str], str],
) -> Optional[Password]:
    """_summary_

    Args:
        password (str): _description_
        add_sult_pepper (Callable[[str],str]): funtion(passwd) -> padding_str, 솔트 패퍼해주는 함수를 넣어준다.

    Returns:
        Optional[Password]: _description_
    """
    import hashlib

    match add_sult_pepper:
        case func if isinstance(func, Callable):
            padding_pw = add_sult_pepper(password)
        case _:
            return None

    hash = hashlib.sha256()
    hash.update(padding_pw.encode("utf-8"))
    hashed_password = hash.hexdigest()
    return Password(pw=hashed_password)
