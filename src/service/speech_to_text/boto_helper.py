import os
from enum import Enum
import boto3
from fastapi import UploadFile, File, Form

class BotoClientEnum(str, Enum):
    transcribe='transcribe'
    s3 = 's3'

class BotoHelper:
    def __init__(self):
        pass

    def upload_to_s3(self, file: UploadFile, file_byte: bytes, bucket:str, key: str):
        s3_client = self._create_client(BotoClientEnum.s3)

        # Upload file to S3
        s3_client.put_object(
            Body=file_byte,
            Bucket=bucket,
            Key=key,
            ContentType=file.content_type
        )

        return f"https://{bucket}.s3.amazonaws.com/{key}"

    @staticmethod
    def _create_client(client_name: BotoClientEnum):
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_DEFAULT_REGION")

        return boto3.client(client_name,
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=secret_key,
                                  region_name=region)