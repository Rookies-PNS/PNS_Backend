import __init__
from typing import Dict, List, Union
from collections.abc import Collection
from icecream import ic

from Domains.Entities import *
from Commons import UserId, Uid


def dict_to_user(user: Dict[str, Union[Dict[str, any], str]]) -> SimpleUser:
    return SimpleUser(
        user_id=UserId(account=user["user_id"]["account"]),
        nickname=user["name"],
        uid=Uid(idx=int(user["uid"]["idx"])),
    )


def user_to_dict(user: SimpleUser) -> Dict[str, str]:
    return {
        "id": str(user.uid.idx),
        "account": user.get_account(),
        "name": user.get_user_nickname(),
    }


def simple_post_to_dict(post: SimplePost) -> Dict[str, str]:
    return {
        "id": str(post.post_id.idx),
        "img_key": str("없음"),
        "title": post.title,
        "target_time": post.target_time.get_time().strftime("%m/%d-%H:%M"),
        "share_flag": post.share_flag,
        "owner": post.get_owner_nickname(),
    }


def post_to_dict(post: PostVO) -> Dict[str, str]:
    return {
        "title": post.title,
        "content": post.get_content(),
        "owner": post.get_owner_nickname(),
        "create_time": post.create_time.get_time().strftime("%m/%d-%H:%M"),
        "update_time": post.update_time.get_time().strftime("%m/%d-%H:%M"),
        "post_id": str(post.post_id.idx),
        "share_flag": post.share_flag,
        "img_key": str("없음"),
    }


def users_to_dicts(users: Collection[SimpleUser]) -> List[Dict[str, str]]:
    return [user_to_dict(u) for u in users]


def posts_to_dicts(
    posts: Collection[Union[PostVO, SimplePost]]
) -> List[Dict[str, str]]:
    ret = []
    for p in posts:
        match p:
            case vo if isinstance(vo, PostVO):
                ret.append(post_to_dict(vo))
            case simple if isinstance(simple, SimplePost):
                ret.append(simple_post_to_dict(simple))
    return ret
