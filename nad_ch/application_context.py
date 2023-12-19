import os
import logging
from nad_ch.config import STORAGE_PATH
from nad_ch.infrastructure.database import (
    session_scope,
    SqlAlchemyDataProviderRepository,
    SqlAlchemyDataSubmissionRepository
)
from nad_ch.infrastructure.logger import Logger
from nad_ch.infrastructure.storage import LocalStorage
from tests.fakes import (
    FakeDataProviderRepository,
    FakeDataSubmissionRepository,
    FakeStorage
)


class ApplicationContext:
    def __init__(self):
        self._providers = SqlAlchemyDataProviderRepository(session_scope)
        self._submissions = SqlAlchemyDataSubmissionRepository(session_scope)
        self._logger = Logger(__name__)
        self._storage = LocalStorage(STORAGE_PATH)

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


class TestApplicationContext(ApplicationContext):
    def __init__(self):
        self._providers = FakeDataProviderRepository()
        self._submissions = FakeDataSubmissionRepository()
        self._logger = Logger(__name__, logging.DEBUG)
        self._storage = FakeStorage()

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


def create_app_context():
    if os.environ.get('APP_ENV') == 'test':
        return TestApplicationContext()
    return ApplicationContext()
