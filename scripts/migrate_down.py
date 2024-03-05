import os
from alembic.config import Config
from alembic import command
from boto3.session import Session
from botocore.client import Config as BotocoreConfig
from nad_ch.config.development_local import (
    S3_ENDPOINT,
    S3_ACCESS_KEY,
    S3_SECRET_ACCESS_KEY,
    S3_BUCKET_NAME,
)


def main():
    if os.getenv("APP_ENV") != "dev_local":
        raise Exception("This script can only be run in a local dev environment.")

    current_script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_script_path))
    alembic_cfg_path = os.path.join(project_root, "alembic.ini")

    alembic_cfg = Config(alembic_cfg_path)
    command.downgrade(alembic_cfg, "base")

    # flush storage
    session = Session()
    minio_client = session.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_ACCESS_KEY,
        aws_session_token=None,
        region_name="us-east-1",
        verify=False,
        config=BotocoreConfig(signature_version="s3v4"),
    )
    response = minio_client.list_objects_v2(Bucket=S3_BUCKET_NAME)

    for object in response["Contents"]:
        print("Deleting", object["Key"])
        minio_client.delete_object(Bucket=S3_BUCKET_NAME, Key=object["Key"])


if __name__ == "__main__":
    main()
