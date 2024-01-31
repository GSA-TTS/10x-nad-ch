import logging
from nad_ch.application.interfaces import Logger, Storage, TaskQueue
import nad_ch.config as config
from nad_ch.domain.repositories import DataProviderRepository, DataSubmissionRepository
from nad_ch.infrastructure.database import (
    create_session_factory,
    SqlAlchemyDataProviderRepository,
    SqlAlchemyDataSubmissionRepository,
)
from nad_ch.infrastructure.logger import BasicLogger
from nad_ch.infrastructure.storage import S3Storage, MinioStorage
from nad_ch.infrastructure.task_queue import celery_app, CeleryTaskQueue
from tests.fakes_and_mocks import (
    FakeDataProviderRepository,
    FakeDataSubmissionRepository,
    FakeStorage,
)


class ApplicationContext:
    def __init__(self):
        self._session = create_session_factory(config.DATABASE_URL)
        self._providers = self.create_provider_repository()
        self._submissions = self.create_submission_repository()
        self._logger = self.create_logger()
        self._storage = self.create_storage()
        self._task_queue = self.create_task_queue()

    def create_provider_repository(self):
        return SqlAlchemyDataProviderRepository(self.session)

    def create_submission_repository(self):
        return SqlAlchemyDataSubmissionRepository(self.session)

    def create_logger(self):
        return BasicLogger(__name__)

    def create_storage(self):
        return S3Storage(
            config.S3_ACCESS_KEY,
            config.S3_SECRET_ACCESS_KEY,
            config.S3_REGION,
            config.S3_BUCKET_NAME,
        )

    def create_task_queue(self):
        return CeleryTaskQueue(celery_app)

    @property
    def providers(self) -> DataProviderRepository:
        return self._providers

    @property
    def submissions(self) -> DataSubmissionRepository:
        return self._submissions

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def storage(self) -> Storage:
        return self._storage

    @property
    def task_queue(self) -> TaskQueue:
        return self._task_queue


class DevLocalApplicationContext(ApplicationContext):
    def create_logger(self):
        return BasicLogger(__name__, logging.DEBUG)

    def create_storage(self):
        return MinioStorage(
            config.S3_ENDPOINT,
            config.S3_ACCESS_KEY,
            config.S3_SECRET_ACCESS_KEY,
            config.S3_BUCKET_NAME,
        )


class TestApplicationContext(ApplicationContext):
    def __init__(self):
        self._session = None
        self._providers = self.create_provider_repository()
        self._submissions = self.create_submission_repository()
        self._logger = self.create_logger()
        self._storage = self.create_storage()
        self._task_queue = self.create_task_queue()

    def create_provider_repository(self):
        return FakeDataProviderRepository()

    def create_submission_repository(self):
        return FakeDataSubmissionRepository()

    def create_logger(self):
        return BasicLogger(__name__, logging.DEBUG)

    def create_storage(self):
        return FakeStorage()


def create_app_context():
    if config.APP_ENV == "test":
        return TestApplicationContext()
    elif config.APP_ENV == "dev_local":
        return DevLocalApplicationContext()
    else:
        return ApplicationContext()
