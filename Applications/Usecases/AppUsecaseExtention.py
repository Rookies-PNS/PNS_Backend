import __init__


def validate_user_input(user_input: str, max_len: int = 50) -> bool:
    """
    회원의 id, name과 게시글의 title을 검증하는 함수
    """
    # 입력이 공백인지 확인
    is_not_empty = bool(user_input.strip())

    # 길이가 200자를 넘지 않는지 확인
    is_not_too_long = len(user_input) <= max_len

    return is_not_empty and is_not_too_long
