import os
import glob
import shutil
import tempfile
from typing import Optional
from zipfile import ZipFile
from boto3.session import Session
from botocore.client import Config
from nad_ch.application.dtos import DownloadResult
from nad_ch.application.interfaces import Storage


class S3Storage(Storage):
    def __init__(
        self, access_key_id: str, secret_access_key: str, region: str, bucket: str
    ):
        session = Session()
        self.client = session.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region,
        )
        self.bucket_name = bucket

    def upload(self, source: str, destination: str) -> bool:
        try:
            self.client.upload_file(source, Bucket=self.bucket_name, Key=destination)
            return True
        except FileNotFoundError:
            return False

    def delete(self, key: str) -> bool:
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except Exception:
            return False

    def download_temp(self, key: str) -> Optional[DownloadResult]:
        try:
            temp_dir = tempfile.mkdtemp()

            zip_file_path = os.path.join(temp_dir, key)
            self.client.download_file(self.bucket_name, key, zip_file_path)
            extracted_dir = f"{temp_dir}_extraced"

            with ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(extracted_dir)

            gdb_dirs = [
                d
                for d in glob.glob(os.path.join(extracted_dir, "*"))
                if os.path.isdir(d) and d.endswith(".gdb")
            ]
            gdb_dir = gdb_dirs[0] if gdb_dirs else None

            return DownloadResult(temp_dir=temp_dir, extracted_dir=gdb_dir)
        except Exception:
            return None

    def cleanup_temp_dir(self, temp_dir: str) -> bool:
        try:
            shutil.rmtree(temp_dir)
            return True
        except Exception:
            return False


class MinioStorage(S3Storage):
    def __init__(
        self, endpoint_url: str, access_key_id: str, secret_access_key: str, bucket: str
    ):
        session = Session()
        self.client = session.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            aws_session_token=None,
            region_name="us-east-1",
            verify=False,
            config=Config(signature_version="s3v4"),
        )
        self.bucket_name = bucket


class LocalStorage(Storage):
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

    def download_temp(self, key: str) -> Optional[DownloadResult]:
        return DownloadResult(temp_dir=key, extracted_dir=f"{key}.gdb")

    def cleanup_temp_dir(self, temp_dir: str) -> bool:
        if temp_dir:
            return True
        else:
            return False
