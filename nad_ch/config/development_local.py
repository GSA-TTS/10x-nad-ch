import logging
import os
from .base import *
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.infrastructure.database import (
    create_session_factory,
    SqlAlchemyDataProducerRepository,
    SqlAlchemyDataSubmissionRepository,
    SqlAlchemyUserRepository,
    SqlAlchemyColumnMapRepository,
    SqlAlchemyRoleRepository,
)
from nad_ch.infrastructure.auth import AuthenticationImplementation
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
TEST_DATABASE_URL = (
    f"postgresql+psycopg2://{postgres_user}:{postgres_password}"
    f"@{postgres_host}:{postgres_port}/test_database"
)
QUEUE_BROKER_URL = os.getenv("QUEUE_BROKER_URL")
QUEUE_BACKEND_URL = os.getenv("QUEUE_BACKEND_URL")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
S3_REGION = os.getenv("S3_REGION")
LANDING_ZONE = os.path.join(os.getcwd(), "data/landing_zone")


class DevLocalApplicationContext(ApplicationContext):
    def __init__(self):
        self._session_factory = create_session_factory(DATABASE_URL)
        self._producers = self.create_producer_repository()
        self._submissions = self.create_submission_repository()
        self._users = self.create_user_repository()
        self._column_maps = self.create_column_map_repository()
        self.roles = self.create_role_repository()
        self._logger = self.create_logger()
        self._storage = self.create_storage()
        self._task_queue = self.create_task_queue()
        self._auth = self.create_auth()

    def create_producer_repository(self):
        return SqlAlchemyDataProducerRepository(self._session_factory)

    def create_submission_repository(self):
        return SqlAlchemyDataSubmissionRepository(self._session_factory)

    def create_user_repository(self):
        return SqlAlchemyUserRepository(self._session_factory)

    def create_column_map_repository(self):
        return SqlAlchemyColumnMapRepository(self._session_factory)

    def create_role_repository(self):
        return SqlAlchemyRoleRepository(self._session_factory)

    def create_logger(self):
        return BasicLogger(__name__, logging.DEBUG)

    @staticmethod
    def create_storage():
        return MinioStorage(
            S3_ENDPOINT,
            S3_ACCESS_KEY,
            S3_SECRET_ACCESS_KEY,
            S3_REGION,
            S3_BUCKET_NAME,
        )

    def create_task_queue(self):
        from nad_ch.infrastructure.task_queue import celery_app, CeleryTaskQueue

        return CeleryTaskQueue(celery_app)

    def create_auth(self):
        return AuthenticationImplementation(
            OAUTH2_CONFIG, ALLOWED_LOGIN_DOMAINS, CALLBACK_URL_SCHEME
        )


def create_app_context():
    return DevLocalApplicationContext()
