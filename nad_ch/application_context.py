import os
from .infrastructure.database import SqlAlchemyDataProviderRepostiory
from tests.mocks import MockDataProviderRepository


class ApplicationContext:
    def __init__(self):
        self._providers = SqlAlchemyDataProviderRepostiory()

    @property
    def providers(self):
        return self._providers


class TestApplicationContext(ApplicationContext):
    def __init__(self):
        self._providers = MockDataProviderRepository()


def create_app_context():
    if os.environ.get('APP_ENV') == 'test':
        return TestApplicationContext()
    return ApplicationContext()
