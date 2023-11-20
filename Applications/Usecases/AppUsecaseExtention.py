import __init__
from dataclasses import dataclass
from typing import Optional

from Domains.Entities import User
from Commons import Password, UserId, Content
from Applications.Results import Result, Fail


def check_valid_password(input_pw: str) -> bool:
    import re

    pattern = re.compile(
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )

    if pattern.match(input_pw):
        return True
    else:
        return False


def convert_to_Password_with_hashing(password: str) -> Optional[Password]:
    import hashlib

    hash = hashlib.sha256()
    hash.update(password.encode("utf-8"))
    hashed_password = hash.hexdigest()
    return Password(pw=hashed_password)


def validate_user_input(user_input: str) -> Result[str]:
    import html

    """
    회원의 id, name과 게시글의 title을 검증하는 함수
    """
    # XSS 방지: HTML 태그 제거
    user_input = html.escape(user_input)

    # CSRF 방지: 특정 문자열이나 패턴을 필터링
    csrf_patterns = ["{{", "}}", "{%", "%}", "<%", "%>", "<$"]
    for pattern in csrf_patterns:
        if pattern in user_input:
            return Fail(type="Fail_Not_Validate_UserInput")

    # SQL Injection 방지: 특수 문자 필터링
    sql_injection_patterns = [";"]
    for pattern in sql_injection_patterns:
        if pattern in user_input.upper():
            return Fail(type="Fail_Not_Validate_UserInput")

    sql_injection_patterns = ["--", "DROP", "DELETE", "UPDATE", "INSERT", "SELECT"]
    for pattern in sql_injection_patterns:
        if pattern in user_input.upper():
            input_text = input_text.replace(pattern, f"`{pattern}`")

    # 기타 사용자 정의 검증 규칙 추가 가능

    # 모든 검증을 통과하면 True 반환
    return user_input


def convert_to_content(board_content: str) -> Result[Content]:
    """
    게시판 content를 검증하고 적절히 변환하는 함수
    """
    # Markdown 코드 블록 안의 코드는 안전하다고 가정하고 HTML 이스케이프 적용
    board_content = process_markdown_code_blocks(board_content)

    # SQL Injection, XSS, CSRF 등 방지를 위한 필터링
    board_content = prevent_security_attacks(board_content)

    return Content(content=board_content)


def process_markdown_code_blocks(input_text: str) -> str:
    import re

    """
    Markdown 코드 블록 안의 코드는 안전하다고 가정하고 HTML 이스케이프 적용
    """
    # Markdown 코드 블록 추출 정규 표현식
    code_block_pattern = re.compile(r"```.*?```", re.DOTALL)

    # 코드 블록 추출
    code_blocks = code_block_pattern.findall(input_text)

    # 코드 블록 안의 코드는 안전하다고 가정하고 HTML 이스케이프 적용
    for code_block in code_blocks:
        input_text = input_text.replace(
            code_block, process_inner_code_block(code_block)
        )

    return input_text


def process_inner_code_block(code_block):
    import re
    import html

    """
    코드 블록 안의 코드는 안전하다고 가정하고 HTML 이스케이프 적용
    """
    # 코드 블록 내 코드 추출 정규 표현식
    code_pattern = re.compile(r"`.*?`")

    # 코드 추출
    codes = code_pattern.findall(code_block)

    # 코드 블록 내 코드는 안전하다고 가정하고 HTML 이스케이프 적용
    for code in codes:
        code_block = code_block.replace(code, f"`{html.escape(code[1:-1])}`")

    return code_block


def prevent_security_attacks(input_text):
    import html

    """
    SQL Injection, XSS, CSRF 등을 방지하기 위한 필터링
    """
    # SQL Injection 방지: 특수 문자 필터링
    sql_injection_patterns = [";", "--", "DROP", "DELETE", "UPDATE", "INSERT", "SELECT"]
    for pattern in sql_injection_patterns:
        input_text = input_text.replace(pattern, f"`{pattern}`")

    # XSS 방지: HTML 태그 이스케이프
    input_text = html.escape(input_text)

    # CSRF 방지: 특정 문자열이나 패턴을 필터링
    csrf_patterns = ["{{", "}}", "{%", "%}", "<%", "%>", "<$"]
    for pattern in csrf_patterns:
        input_text = input_text.replace(pattern, f"`{pattern}`")

    return input_text
