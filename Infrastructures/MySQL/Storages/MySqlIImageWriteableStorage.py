import __init__
from typing import Optional
from collections.abc import Collection
import boto3
from flask import current_app
from Commons import *
from Domains.Entities import User, UserVO, SimpleUser, SecuritySimpleUser
from Applications.Results import Result, Fail
from Applications.Repositories.Interfaces import (
    IPostWriteableRepository,
    IImageWriteableRepository,
)
from botocore.exceptions import NoCredentialsError
from icecream import ic
import pymysql


class MySqlIImageWritableStorage(IImageWriteableRepository):
    def upload_to_s3(file, bucket_name, object_name) -> Optional[Fail]:
        ic(object_name)
        # AWS S3 클라이언트 생성
        s3 = boto3.client("s3")
        try:
            # 파일 객체를 S3 버킷에 업로드
            s3.upload_fileobj(
                file,
                bucket_name,
                object_name,
                ExtraArgs={"ACL": "public-read"},
            )
            return True
        except Exception as e:
            print("An error occurred: ", e)
            return False

    def get_s3_url(bucket_name, object_name):
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        return s3_url

    def save_image_data(user_id, s3_url) -> Result[ImageKey]:
        # 데이터베이스 연결 설정
        from get_db_data import get_mysql_dict

        sql_config = get_mysql_dict()
        connection = pymysql.connect(
            host=sql_config["host"],
            user=sql_config["user"],
            password=sql_config["password"],
            db=sql_config["database"],
            charset=sql_config["charset"],
            cursorclass=pymysql.cursors.DictCursor,
        )

        try:
            with connection.cursor() as cursor:
                # 이미지 URL을 저장하는 쿼리
                sql = "INSERT INTO your_image_table (url, user_id) VALUES (%s, %s)"
                cursor.execute(sql, (user_id, s3_url))

            # 변경 사항을 데이터베이스에 반영
            connection.commit()
        except Exception as e:
            print("An error occurred while saving image data: ", e)
            return False
        finally:
            connection.close()

        return True
