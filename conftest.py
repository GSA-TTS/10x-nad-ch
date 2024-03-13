from tests.fixtures import *
from tests.test_data.baselines import *
from nad_ch.config import QUEUE_BACKEND_URL, QUEUE_BROKER_URL


pytest_plugins = ("celery.contrib.pytest", )


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": QUEUE_BROKER_URL,
        "result_backend": QUEUE_BACKEND_URL,
        "broker_connection_retry": True,
        "broker_connection_retry_delay": 5,
        "broker_connection_retry_max": 3,
        "broker_connection_retry_on_startup": True
    }
