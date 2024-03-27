import logging
import os
from .base import OAUTH2_CONFIG, ALLOWED_LOGIN_DOMAINS, CALLBACK_URL_SCHEME
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.infrastructure.logger import BasicLogger
from tests.fakes_and_mocks import (
    FakeAuth,
    FakeDataProducerRepository,
    FakeDataSubmissionRepository,
    FakeUserRepository,
    FakeColumnMapRepository,
    FakeStorage,
)


DATABASE_URL = os.getenv("DATABASE_URL")
QUEUE_BROKER_URL = os.getenv("QUEUE_BROKER_URL")
QUEUE_BACKEND_URL = os.getenv("QUEUE_BACKEND_URL")
LANDING_ZONE = os.path.join(os.getcwd(), "data/landing_zone")


class TestApplicationContext(ApplicationContext):
    def __init__(self):
        self._session = None
        self._producers = self.create_producer_repository()
        self._submissions = self.create_submission_repository()
        self._users = self.create_user_repository()
        self._column_maps = self.create_column_map_repository()
        self._logger = self.create_logger()
        self._storage = self.create_storage()
        self._task_queue = self.create_task_queue()
        self._auth = self.create_auth()

    def create_producer_repository(self):
        return FakeDataProducerRepository()

    def create_submission_repository(self):
        return FakeDataSubmissionRepository()

    def create_user_repository(self):
        return FakeUserRepository()

    def create_column_map_repository(self):
        return FakeColumnMapRepository()

    def create_logger(self):
        return BasicLogger(__name__, logging.DEBUG)

    @staticmethod
    def create_storage():
        return FakeStorage()

    def create_task_queue(self):
        from nad_ch.infrastructure.task_queue import celery_app, CeleryTaskQueue

        return CeleryTaskQueue(celery_app)

    def create_auth(self):
        return FakeAuth(
            {
                "test": {
                    "client_id": "test_client_id",
                    "client_secret": "test_client_secret",
                    "authorize_url": "https://test.org/oauth/authorize",
                    "token_url": "https://test.org/oauth/token",
                    "logout_url": "https://test.org/logout",
                    "userinfo": {
                        "url": "access_token",
                        "email": lambda json: json["email"],
                    },
                    "scopes": ["openid"],
                }
            },
            ALLOWED_LOGIN_DOMAINS,
            CALLBACK_URL_SCHEME,
        )


def create_app_context():
    return TestApplicationContext()
