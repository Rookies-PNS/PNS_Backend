# PNS_Backend
공유 일기 프로젝트 입니다. 회원에 대한 CRUD, 일기에 대한 CRUD 구현합니다. 계정 별로 다양한 권한을 부여합니다.

# Requirements
```bash
# python<=3.11
pip install -r requirements.txt
```

# How to Start

## Download Code
```bash
git clone https://github.com/Rookies-PNS/PNS_Backend.git
cd PNS_Backend
pip install -r requirments.txt
```

### Make secrets.json and db_config.py
`secrets.json`
```json
{
    "SECRET_KEY": "YOUR_SECRET_KEY"
}
```

`mysql_config.py`
```python
mysql_db = {
    "user": "USER_NAME",
    "password": "DB_PASSWORD",
    "host": "localhost",
    "port": "3306",
    "database": "DATABASE_NAME",
    "charset": "utf8",
}
```

### Set MySQL
1. `download` mysql and base setting
2. `create` mysql user and database (root로 만들면, 유저관련은 생략가능)
   ```sql
    create database "DATABASE_NAME";
    create user "USER_NAME"@localhost identified by 'DB_PASSWORD';
    grant all privilege on "DATABASE_NAME".* to 'USER_NAME'@'localhost';
   ```
3. `run` manage.py (DB 테이블 생성과, 초기 계정&일기 생성)
    ```bash
    python manage.py --run migrate
    ```

# How to Run
### debug mode
```bash
python manage.py --debug
python3.11 manage.py --debug

```

### service mode
```bash
python manage.py --host x.x.x.x --port 5000
python3.11 manage.py --host x.x.x.x --port 5000
```

# How to Test
```bash
python manage.py --run test
python3.11 manage.py --run test
```

# How to Auto Git Push
```bash
python manage.py --run git-push
python3.11 manage.py --run git-push
```

# `init_data.py` 생성방법 예시

### `def init_user()`
```python
def init_user():
    from Commons import Auth, Policy, TargetScope
    from Applications.Usecases.UserServices import CreateUserService
    from Domains.Entities.User import SimpleUser
    from Infrastructures.IOC import get_strage_factory
    from Infrastructures.Interfaces import IStorageFactory
    from Applications.Repositories.Interfaces import IUserWriteableRepository
    from icecream import ic

    users = [
        {
        # 관리자 권한
        "id": "PostAdmin",
        "pw": "Admin123!@",
        "name": "PostAdmin",
        "nick": "post_admini",
        "auth": [
            Auth(Policy.PostReadAblePolicy, TargetScope.Allowed),  # 공개된 일기 읽기 가능
            Auth(Policy.UserDataReadAblePolicy, TargetScope.Own),  # 자신의 유저 정보 열람가능
            Auth(Policy.PostPrivateAblePolicy, TargetScope.All),  # 모든 일기 비공개가능
            Auth(
                Policy.UserAuthLockOfPostPublicPolicy, TargetScope.All
            ),  # 모든 유저 일기공개 권한정지 권한
            Auth(
                Policy.UserAuthUnlockOfPostPublicPolicy, TargetScope.All
            ),  # 모든 유저 일기공개 권한정지 해제 권한
            Auth(Policy.UserDataReadAblePolicy, TargetScope.All),  # 모든 유저 정보 열람가
            Auth(Policy.UserDataDeleteAblePolicy, TargetScope.Own),  # 자기 계정 삭제가능
            ],
        },
        # 일반사용자 권한
        {
            "id": "nomal_id",
            "pw": "1qaz2wsx!@QW",
            "name": "nomaluser",
            "nick": "nomals",
            "auth": [
                Auth(Policy.UserDataReadAblePolicy, TargetScope.Own),  # 자신의 유저 정보 열람가능
                Auth(Policy.UserDataDeleteAblePolicy, TargetScope.Own),  # 자기 계정 삭제가능
                Auth(Policy.PostReadAblePolicy, TargetScope.Allowed),  # 공개된 일기 읽기 가능
                Auth(Policy.PostReadAblePolicy, TargetScope.Own),  # 자기 일기 읽기 가능
                Auth(Policy.PostDeleteAblePolicy, TargetScope.Own),  # 자기 일기 삭제가능
                Auth(Policy.PostCreateAndUpdateAblePolicy, TargetScope.Own),  # 자기 일기 수정가능
                Auth(Policy.PostPublicAblePolicy, TargetScope.Own),  # 자기 일기 공개가능
                Auth(Policy.PostPrivateAblePolicy, TargetScope.Own),  # 자기 일기 비공개가능
            ],
        }

    ]

    
    service = CreateUserService(get_strage_factory().get_user_write_storage())

    for user in users:
        ret = service.create(
            account=user["id"],
            passwd=user["pw"],
            name=user["name"],
            nickname=user["nick"],
            auths=user["auth"],
        )
        match ret:
            case none if none is None:
                ic("Succuss")
            case _:
                ic("Fail", ret)
```

### `def init_post()`
```python
def init_post():
    from Applications.Usecases.UserServices import LoginService
    from Applications.Usecases.PostServices import CreatePostService
    from Domains.Entities import SimplePost
    from Infrastructures.IOC import get_post_storage, get_user_storage
    from Infrastructures.Interfaces import IStorageFactory
    from Applications.Repositories.Interfaces import (
        IUserWriteableRepository,
        IPostWriteableRepository,
    )
    from datetime import datetime, timedelta

    now = datetime.now()
    now = now.replace(microsecond=0)

    (repoW, repoR) = get_user_storage()
    login = LoginService(repoR, repoW)
    nomal = login.login("nomal_id", "1qaz2wsx!@QW")
    create = CreatePostService(get_post_storage()[0], repoW)

    start = {
        "title": "사이트의 시작을 알립니다.",
        "content": f"""이 사이트는 {now.strftime("%Y/%m/%d")}에 시작했습니다.
이용자 여러분 앞으로 잘 부탁드립니다.""",
        "user": nomal,
        "time": now,
        "flag": False,
    }
    now = now + timedelta(minutes=5)
    anony_post = {
        "title": "여기 짱이 누구냐",
        "content": f"""짜잔! 내가 등장했다!!
이 게시판은 내가 먹도록 하겠다.""",
        "user": nomal,
        "time": now,
        "flag": True,
    }

    posts = [
        start,
        anony_post,
    ]
    for post in posts:
        create.create(
            title=post["title"],
            content=post["content"],
            create_time=post["time"],
            user=post["user"],
            share_flag=False,
            target_time=datetime.now(),
            img=None,
        )
```

# 주요기능

## 회원기능 개요
1. 비회원 ( 회원가입, 로그인 )
2. 일반회원 ( 일기쓰기, 공유일기 읽기, 본인 일기 삭제, 본인 일기 조회 )
3. 계정관리자 ( 공유일기 읽기, 모든 일기 삭제 )

## 권한 관리
1. 비회원의 일기 접근 금지
2. 일반회원의 본인 소유일기와 공유일기를 제외한 타인의 일기 읽기 금지
3. 일기를 소유한 회원과 계정관리자를 제외한 사용자가 삭제 금지