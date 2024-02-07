from celery import Celery
import geopandas as gpd
from nad_ch.application.dtos import (
    DataSubmissionReport,
    DataSubmissionReportOverview,
    DataSubmissionReportFeature,
)
from nad_ch.application.interfaces import TaskQueue
from nad_ch.application.validation import get_feature_count
from nad_ch.config import QUEUE_BROKER_URL, QUEUE_BACKEND_URL
from nad_ch.domain.repositories import DataSubmissionRepository


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
def load_and_validate(gdb_file_path: str) -> dict:
    gdf = gpd.read_file(gdb_file_path)
    overview = DataSubmissionReportOverview(feature_count=get_feature_count(gdf))
    report = DataSubmissionReport(overview)
    return report.to_dict()


class CeleryTaskQueue(TaskQueue):
    def __init__(self, app):
        self.app = app

    def run_load_and_validate(
        self, submissions: DataSubmissionRepository, submission_id: int, path: str
    ):
        task_result = load_and_validate.apply_async(args=[path])
        report_dict = task_result.get()
        submissions.update_report(submission_id, report_dict)
        return DataSubmissionReport(**report_dict)
