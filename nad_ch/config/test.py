import logging
import os
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.infrastructure.logger import BasicLogger
from tests.fakes_and_mocks import (
    FakeDataProducerRepository,
    FakeDataSubmissionRepository,
    FakeStorage,
)


DATABASE_URL = os.getenv("DATABASE_URL")
QUEUE_BROKER_URL = os.getenv("QUEUE_BROKER_URL")
QUEUE_BACKEND_URL = os.getenv("QUEUE_BACKEND_URL")


class TestApplicationContext(ApplicationContext):
    def __init__(self):
        self._session = None
        self._producers = self.create_producer_repository()
        self._submissions = self.create_submission_repository()
        self._logger = self.create_logger()
        self._storage = self.create_storage()
        self._task_queue = self.create_task_queue()

    def create_producer_repository(self):
        return FakeDataProducerRepository()

    def create_submission_repository(self):
        return FakeDataSubmissionRepository()

    def create_logger(self):
        return BasicLogger(__name__, logging.DEBUG)

    def create_storage(self):
        return FakeStorage()

    def create_task_queue(self):
        from nad_ch.infrastructure.task_queue import celery_app, CeleryTaskQueue

        return CeleryTaskQueue(celery_app)


def create_app_context():
    return TestApplicationContext()
