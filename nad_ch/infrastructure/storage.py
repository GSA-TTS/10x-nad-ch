import os
import boto3
import shutil


class S3Storage:
    def __init__(self, access_key_id: str, secret_access_key: str, region: str,
                 bucket: str):
        self.s3client = boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region,
        )
        self.bucket_name = bucket

    def upload(self, source: str, destination: str) -> bool:
        try:
            self.s3client.upload_file(source, Bucket=self.bucket, Key=destination)
            return True
        except FileNotFoundError:
            return False

    def delete(self, s3_key) -> bool:
        try:
            self.s3client.delete_object(Bucket=self.bucket, Key=s3_key)
            return True
        except Exception:
            return False


class LocalStorage:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def _full_path(self, path: str) -> str:
        return os.path.join(self.base_path, path)

    def upload(self, source: str, destination: str) -> bool:
        shutil.copy(source, self._full_path(destination))
        return True

    def delete(self, file_path: str) -> bool:
        full_file_path = self._full_path(file_path)
        if os.path.exists(full_file_path):
            os.remove(full_file_path)
            return True
        else:
            return False
