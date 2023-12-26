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

[회원기능](https://github.com/Rookies-PNS/PNS_Backend/blob/main/Applications/README.md)


# TimeLine

[진행상황](https://docs.google.com/spreadsheets/d/12uU9tzwKI6kATs_Ijud8bKqW2Ijg9RNQYvF_wUSeZ-M/edit#gid=1490708584)
