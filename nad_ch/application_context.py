import os
from .gateways.storage_mock import StorageGatewayMock

class ApplicationContext:
    def __init__(self):
        self._storage = StorageGatewayMock()

    @property
    def storage(self):
        return self._storage

class TestApplicationContext(ApplicationContext):
    def __init__(self):
        self._storage = StorageGatewayMock()

def create_app_context():
    if os.environ.get('APP_ENV') == 'test':
        return TestApplicationContext()
    return ApplicationContext()
