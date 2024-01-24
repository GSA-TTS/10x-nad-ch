import logging
import nad_ch.config as config
from nad_ch.infrastructure.database import (
    create_session_factory,
    SqlAlchemyDataProviderRepository,
    SqlAlchemyDataSubmissionRepository,
)
from nad_ch.infrastructure.logger import Logger
from nad_ch.infrastructure.storage import LocalStorage, S3Storage
from nad_ch.infrastructure.task_queue import LocalTaskQueue, RedisTaskQueue
from tests.fakes import (
    FakeDataProviderRepository,
    FakeDataSubmissionRepository,
    FakeStorage,
)


class ApplicationContext:
    def __init__(self):
        self._providers = self.create_provider_repository()
        self._submissions = self.create_submission_repository()
        self._logger = self.create_logger()
        self._storage = self.create_storage()
        self._task_queue = self.create_task_queue()

    def create_provider_repository(self):
        return SqlAlchemyDataProviderRepository(
            create_session_factory(config.DATABASE_URL)
        )

    def create_submission_repository(self):
        return SqlAlchemyDataSubmissionRepository(
            create_session_factory(config.DATABASE_URL)
        )

    def create_logger(self):
        return Logger(__name__)

    def create_storage(self):
        return S3Storage(
            config.S3_ACCESS_KEY,
            config.S3_SECRET_ACCESS_KEY,
            config.S3_REGION,
            config.S3_BUCKET_NAME,
        )

    def create_task_queue(self):
        return RedisTaskQueue(
            "task-queue", config.QUEUE_PASSWORD, config.QUEUE_HOST, config.QUEUE_PORT
        )

    @property
    def providers(self):
        return self._providers

    @property
    def submissions(self):
        return self._submissions

    @property
    def logger(self):
        return self._logger

    @property
    def storage(self):
        return self._storage

    @property
    def task_queue(self):
        return self._task_queue


class DevLocalApplicationContext(ApplicationContext):
    def create_provider_repository(self):
        return SqlAlchemyDataProviderRepository(
            create_session_factory(config.DATABASE_URL)
        )

    def create_submission_repository(self):
        return SqlAlchemyDataSubmissionRepository(
            create_session_factory(config.DATABASE_URL)
        )

    def create_logger(self):
        return Logger(__name__, logging.DEBUG)

    def create_storage(self):
        return LocalStorage(config.STORAGE_PATH)

    def create_task_queue(self):
        return LocalTaskQueue(
            "local-task-queue", config.QUEUE_BROKER_URL, config.QUEUE_BACKEND_URL
        )


class TestApplicationContext(ApplicationContext):
    def create_provider_repository(self):
        return FakeDataProviderRepository()

    def create_submission_repository(self):
        return FakeDataSubmissionRepository()

    def create_logger(self):
        return Logger(__name__, logging.DEBUG)

    def create_storage(self):
        return FakeStorage()

    def create_task_queue(self):
        return LocalTaskQueue(
            "test-task-queue", config.QUEUE_BROKER_URL, config.QUEUE_BACKEND_URL
        )


def create_app_context():
    if config.APP_ENV == "test":
        return TestApplicationContext()
    elif config.APP_ENV == "dev_local":
        return DevLocalApplicationContext()
    else:
        return ApplicationContext()
