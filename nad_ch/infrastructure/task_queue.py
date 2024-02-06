import os
from celery import Celery
import geopandas as gpd
from nad_ch.application.interfaces import TaskQueue
from nad_ch.application.validation import get_feature_count


QUEUE_BROKER_URL = os.getenv("QUEUE_BROKER_URL")
QUEUE_BACKEND_URL = os.getenv("QUEUE_BACKEND_URL")


celery_app = Celery(
    "redis-task-queue", broker=QUEUE_BROKER_URL, backend=QUEUE_BACKEND_URL
)


celery_app.conf.update(
    store_processed=True,
    result_persistent=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)


@celery_app.task
def load_and_validate(gdb_file_path: str) -> int:
    gdf = gpd.read_file(gdb_file_path)
    feature_count = get_feature_count(gdf)
    return feature_count


class CeleryTaskQueue(TaskQueue):
    def __init__(self, app):
        self.app = app

    def run_load_and_validate(self, path: str):
        task_result = load_and_validate.apply_async(args=[path])
        return task_result
