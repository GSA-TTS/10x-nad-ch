import json
import os
from .base import *
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.infrastructure.database import (
    create_session_factory,
    SqlAlchemyDataProviderRepository,
    SqlAlchemyDataSubmissionRepository,
)
from nad_ch.infrastructure.logger import BasicLogger
from nad_ch.infrastructure.storage import S3Storage
from nad_ch.infrastructure.task_queue import celery_app, CeleryTaskQueue


def get_credentials(service_name, default={}):
    service = vcap_services.get(service_name, [default])
    return service[0].get("credentials", default) if service else default


# Remote development config
vcap_services = json.loads(os.getenv("VCAP_SERVICES", "{}"))


postgres_credentials = get_credentials("aws-rds")
redis_credentials = get_credentials("aws-elasticache-redis")
s3_credentials = get_credentials("s3")


DATABASE_URL = postgres_credentials.get("uri", os.getenv("DATABASE_URL"))
QUEUE_HOST = redis_credentials.get("hostname", os.getenv("QUEUE_HOST"))
QUEUE_PORT = redis_credentials.get("port", os.getenv("QUEUE_PORT"))
QUEUE_PASSWORD = redis_credentials.get("password", os.getenv("QUEUE_PASSWORD"))
S3_BUCKET_NAME = s3_credentials.get("bucket", os.getenv("S3_BUCKET_NAME"))
S3_ENDPOINT = s3_credentials.get("endpoint", os.getenv("S3_ENDPOINT"))
S3_ACCESS_KEY = s3_credentials.get("access_key_id", os.getenv("S3_ACCESS_KEY"))
S3_SECRET_ACCESS_KEY = s3_credentials.get(
    "secret_access_key", os.getenv("S3_SECRET_ACCESS_KEY")
)
S3_REGION = s3_credentials.get("region", os.getenv("S3_REGION"))


class DevRemoteApplicationContext(ApplicationContext):
    def __init__(self):
        self._session = create_session_factory(DATABASE_URL)
        self._providers = self.create_provider_repository()
        self._submissions = self.create_submission_repository()
        self._logger = self.create_logger()
        self._storage = self.create_storage()
        self._task_queue = self.create_task_queue()

    def create_provider_repository(self):
        return SqlAlchemyDataProviderRepository(self._session)

    def create_submission_repository(self):
        return SqlAlchemyDataSubmissionRepository(self._session)

    def create_logger(self):
        return BasicLogger(__name__)

    def create_storage(self):
        return S3Storage(
            S3_ACCESS_KEY,
            S3_SECRET_ACCESS_KEY,
            S3_REGION,
            S3_BUCKET_NAME,
        )

    def create_task_queue(self):
        return CeleryTaskQueue(celery_app)


def create_app_context():
    return DevRemoteApplicationContext()
