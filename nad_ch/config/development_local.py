import logging
import os
from .base import *
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.infrastructure.database import (
    create_session_factory,
    SqlAlchemyDataProviderRepository,
    SqlAlchemyDataSubmissionRepository,
)
from nad_ch.infrastructure.logger import BasicLogger
from nad_ch.infrastructure.storage import MinioStorage


STORAGE_PATH = os.getenv("STORAGE_PATH")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_db = os.getenv("POSTGRES_DB")
DATABASE_URL = (
    f"postgresql+psycopg2://{postgres_user}:{postgres_password}"
    f"@{postgres_host}:{postgres_port}/{postgres_db}"
)
QUEUE_BROKER_URL = os.getenv("QUEUE_BROKER_URL")
QUEUE_BACKEND_URL = os.getenv("QUEUE_BACKEND_URL")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
S3_REGION = os.getenv("S3_REGION")


class DevLocalApplicationContext(ApplicationContext):
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
        return BasicLogger(__name__, logging.DEBUG)

    def create_storage(self):
        return MinioStorage(
            S3_ENDPOINT,
            S3_ACCESS_KEY,
            S3_SECRET_ACCESS_KEY,
            S3_BUCKET_NAME,
        )

    def create_task_queue(self):
        from nad_ch.infrastructure.task_queue import celery_app, CeleryTaskQueue

        return CeleryTaskQueue(celery_app)


def create_app_context():
    return DevLocalApplicationContext()
