import __init__
from typing import Dict,List, Union
from collections.abc import Collection
from icecream import ic

from Domains.Entities import *


def user_to_dict(user:SimpleUser)->Dict[str, str]:
    ic()
    ic(user)
    return {
        "id" : str(user.uid.idx),
        "account" : user.user_id.account,
        "name" : user.name,
    }

def simple_post_to_dict(post:SimplePost)->Dict[str,str]:
    ic()
    ic(post)
    return {
        "id": str(post.post_id.idx) ,
        "title": post.title ,
        "user_account": post.get_account() ,
        "create_time": post.create_time.get_time().strftime("%Y/%m/%d - %H:%M:%S") ,
        "update_time": post.update_time.get_time().strftime("%Y/%m/%d - %H:%M:%S")  ,
    }
def post_to_dict(post:PostVO)->Dict[str,str]:
    ic()
    ic(post)
    return {
        "id": str(post.post_id.idx) ,
        "title": post.title ,
        "content": post.get_content(),
        "user_account": post.get_account() ,
        "create_time": post.create_time.get_time().strftime("%Y/%m/%d - %H:%M:%S") ,
        "update_time": post.update_time.get_time().strftime("%Y/%m/%d - %H:%M:%S")  ,
    }

def users_to_dicts(users:Collection[SimpleUser])->List[Dict[str,str]]:
    return[
        user_to_dict(u) for u in users
    ]

def posts_to_dicts(posts:Collection[Union[PostVO,SimplePost]])->List[Dict[str,str]]:
    ic()
    ic(posts)
    ret = []
    for p in posts:
        match p:
            case vo if isinstance(vo, PostVO):
                ret.append(post_to_dict(vo))
            case simple if isinstance(simple, SimplePost):
                ret.append(simple_post_to_dict(simple))
    return ret