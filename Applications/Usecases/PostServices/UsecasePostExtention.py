import __init__

from Commons import Content
from Applications.Results import Result


def convert_to_content(board_content: str) -> Result[Content]:
    """
    게시판 content를 검증하고 적절히 변환하는 함수
    """
    return Content(content=board_content)
