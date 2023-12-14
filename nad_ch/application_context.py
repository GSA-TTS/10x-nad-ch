import os
import logging
from nad_ch.infrastructure.database import (
    session_scope,
    SqlAlchemyDataProviderRepository
)
from nad_ch.infrastructure.logger import Logger
from tests.mocks import MockDataProviderRepository


class ApplicationContext:
    def __init__(self):
        self._providers = SqlAlchemyDataProviderRepository(session_scope)
        self._logger = Logger(__name__)

    @property
    def providers(self):
        return self._providers

    @property
    def logger(self):
        return self._logger


class TestApplicationContext(ApplicationContext):
    def __init__(self):
        self._providers = MockDataProviderRepository()
        self._logger = Logger(__name__, logging.DEBUG)

    @property
    def providers(self):
        return self._providers

    @property
    def logger(self):
        return self._logger


def create_app_context():
    if os.environ.get('APP_ENV') == 'test':
        return TestApplicationContext()
    return ApplicationContext()
