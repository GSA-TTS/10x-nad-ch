import os
from .infrastructure.database import session_scope, SqlAlchemyDataProviderRepository
from tests.mocks import MockDataProviderRepository


class ApplicationContext:
    def __init__(self):
        self._providers = SqlAlchemyDataProviderRepository(session_scope)

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
