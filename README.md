# Log_Board_Tak
간단한 게시판을 만드는 프로젝트 입니다. Flask를 사용하여 로그인 기능, 게시글 작성 및 확인 기능, 회원 권한으로 게시글 작성 기능을 구현합니다.

# Requirements
```bash
# python<=3.11
pip install -r requirements.txt
```

# How to Start

## Download Code
```bash
git clone https://github.com/Cloud-is-best-beer/Log_Board_Tak.git
cd Log_Board_Tak
pip install -r requirments.txt
```

### Make secrets.json and db_config.py
`secrets.json`
```json
{
    "SECRET_KEY": "YOUR_SECRET_KEY"
}
```

`db_config.py`
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
2. `create` mysql user and database
   ```sql
    create database "DATABASE_NAME";
    create user "USER_NAME"@localhost identified by 'DB_PASSWORD';
    grant all privilege on "DATABASE_NAME".* to 'USER_NAME'@'localhost';
   ```
3. `run` manage.py
    ```bash
    python manage.py --run migrate
    ```

# How to Run
### debug mode
```bash
python manage.py
```

### service mode
```bash
python manage.py --not-debug
```

### 기본제공 ID(테스트용)
```bash
ID : admin
PW : Admin123!@
```

# How to Test
```bash
python manage.py --run test
```

# How to Auto Git Push
```bash
python manage.py --run git-push
```

# Docs

[회원기능](https://github.com/Cloud-is-best-beer/Log_Board_Tak/blob/main/Applications/README.md)


# TimeLine

[이탁균 진행상황](https://docs.google.com/spreadsheets/d/1lDSmwstYR6058RaqRJcVM6E0k69j6pXSGbfq7WrgrpE/edit#gid=386990213)