import os
from celery import Celery


class RedisTaskQueue:
    def __init__(self, name: str, password: str, host: str, port: str):
        redis_url = f"redis://:{password}@{host}:{port}/0"

        self.app = Celery(name, broker=redis_url, backend=redis_url)

        self.app.conf.update(
            task_serializer="json", result_serializer="json", accept_content=["json"]
        )

    def define_task(self, func):
        return self.app.task(func)

    def start_worker(self):
        self.app.worker_main(argv=["worker", "--loglevel=info"])


class LocalTaskQueue:
    def __init__(self, name, base_path, backend_url):
        broker_base_path = os.path.join(base_path, "celery_broker")
        broker_url = f"filesystem://{broker_base_path}"

        self.app = Celery(name, broker=broker_url, backend=backend_url)

        self.app.conf.update(
            broker_transport_options={
                "data_folder_in": os.path.join(broker_base_path, "in"),
                "data_folder_out": os.path.join(broker_base_path, "out"),
                "data_folder_processed": os.path.join(broker_base_path, "processed"),
            },
            result_persistent=True,
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],
        )

        os.makedirs(os.path.join(broker_base_path, "in"), exist_ok=True)
        os.makedirs(os.path.join(broker_base_path, "out"), exist_ok=True)
        os.makedirs(os.path.join(broker_base_path, "processed"), exist_ok=True)

    def define_task(self, func):
        return self.app.task(func)

    def start_worker(self):
        self.app.worker_main(argv=["worker", "--loglevel=info"])
