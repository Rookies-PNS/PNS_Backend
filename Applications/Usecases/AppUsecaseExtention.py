import __init__
from Applications.Results import Result, Fail


def validate_user_input(user_input: str, max_len: int = 50) -> Result[str]:
    """
    회원의 id, name과 게시글의 title을 검증하는 함수
    """
    if len(user_input) > max_len:
        return Fail(type="Fail_InvalidateUserInput_ToMush")

    return user_input
