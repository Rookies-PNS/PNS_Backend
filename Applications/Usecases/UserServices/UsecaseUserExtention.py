import __init__
from typing import Optional, Callable, Final
import re
from Commons import Password

account_len: Final = 20
name_len: Final = 35
nickname_len: Final = 20


def check_valid_password(input_pw: str) -> bool:
    pattern = re.compile(
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )

    if pattern.match(input_pw):
        return True
    else:
        return False


def validate_account(account: str) -> bool:
    """
    사용자의 account를 정규표현식으로 검증하는 함수
    """
    # 최소 길이 6, 최대 길이 20
    if not re.match(
        r"^[a-zA-Z0-9!@%*()_+\[\]:?~]{6," + str(account_len) + "}$",
        account,
    ):
        return False
    return True


def validate_name(name: str) -> bool:
    """
    사용자의 이름을 정규표현식으로 검증하는 함수
    """
    # 알파벳 대소문자와 공백만 허용, 최소 2자, 최대 50자
    if re.match(r"^[a-zA-Z ]{2," + str(name_len) + r"}$", name):
        return True
    else:
        return False


def validate_nickname(nickname: str) -> bool:
    """
    사용자의 닉네임을 정규표현식으로 검증하는 함수
    """
    # 알파벳 대소문자와 숫자만 허용, 최소 3자, 최대 20자
    if re.match(r"^[a-zA-Z0-9]{3," + str(nickname_len) + r"}$", nickname):
        return True
    else:
        return False


def get_padding_adder(account: str) -> Callable[[str], str]:
    """_summary_
    특별한 솔트 페퍼를 추가하는 함수를 만들어 주는 함수

    Args:
        account (str): 사용자 고유의 계정
        nickname (str): 사용자 고유의 닉네임

    Returns:
        Callable[[str], str]: funtion(passwd) -> padding_str, 솔트 패퍼해주는 함수를 반환한다.
    """
    before = f"!$&*%?S@1t{account}{account[::-1]}6"
    after = f"9{account[::-1]}{account}P3pp3r?%*&$!"

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
