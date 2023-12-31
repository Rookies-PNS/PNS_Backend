import __init__
from typing import Optional, Callable, Final
import re
from Commons import Password

account_len: Final = 20
name_len: Final = 20
nickname_len: Final = 20


def check_valid_password(input_pw: str) -> bool:
    pattern = re.compile(
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,50}$"
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
        r"^[a-zA-Z0-9!@%*()_+:?~]{6," + str(account_len) + r"}$",
        account,
    ):
        return False
    return True


def validate_name(name: str) -> bool:
    """
    사용자의 이름을 정규표현식으로 검증하는 함수
    # 이름은 한글 또는 영문 대소문자로만 구성되어야 함
    # 중간에 띄어쓰기가 포함될 수 없음
    # 처음과 끝에는 띄어쓰기가 포함되면 안됨
    # 자리수는 2자 이상 20자 이하여야 함
    """
    pattern = re.compile(
        r"^[가-힣a-zA-Z]{2," + str(name_len) + r"}([가-힣a-zA-Z\s]*[가-힣a-zA-Z]+)?$"
    )

    # 정규식에 매칭되는지 확인
    return bool(pattern.match(name))


def validate_nickname(nickname: str) -> bool:
    """
    사용자의 닉네임을 정규표현식으로 검증하는 함수
    # 닉네임은 한글, 영문 대소문자, 특수문자(!@%*()_+?~)로만 구성되어야 함
    # 중간에 띄어쓰기가 포함될 수 없음
    # 처음과 끝에는 띄어쓰기가 포함되면 안됨
    # 자리수는 5자 이상 20자 이하여야 함
    """
    pattern = re.compile(
        r"^[가-힣a-zA-Z!@%*()_+?~]{1,"
        + str(nickname_len)
        + r"}([가-힣a-zA-Z\s]*[가-힣a-zA-Z]+)?$"
    )

    # 정규식에 매칭되는지 확인
    return bool(pattern.match(nickname))


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
