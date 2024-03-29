from celery import Celery
from nad_ch.application.dtos import (
    DataSubmissionReport,
    report_to_dict,
    report_from_dict,
)
from nad_ch.application.data_reader import DataReader
from nad_ch.application.interfaces import TaskQueue
from nad_ch.application.validation import DataValidator
from nad_ch.config import QUEUE_BROKER_URL, QUEUE_BACKEND_URL
from nad_ch.core.repositories import DataSubmissionRepository
from typing import Dict


celery_app = Celery(
    "redis-task-queue",
    broker=QUEUE_BROKER_URL,
    backend=QUEUE_BACKEND_URL,
    broker_connection_retry=True,  # Enable broker connection retry
    broker_connection_retry_delay=5,  # Optional: retry delay in seconds
    broker_connection_retry_max=3,  # Optional: maximum number of retries
    broker_connection_retry_on_startup=True,  # Enable retry on startup
)


celery_app.conf.update(
    store_processed=True,
    result_persistent=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)


@celery_app.task
def load_and_validate(gdb_file_path: str, column_map: Dict[str, str]) -> dict:
    data_reader = DataReader(column_map)
    first_batch = True
    for gdf in data_reader.read_file_in_batches(path=gdb_file_path):
        if first_batch:
            data_validator = DataValidator(data_reader.valid_renames)
        data_validator.run(gdf)
        first_batch = False
    data_validator.finalize_overview_details()
    report = DataSubmissionReport(
        data_validator.report_overview, list(data_validator.report_features.values())
    )
    return report_to_dict(report)


class CeleryTaskQueue(TaskQueue):
    def __init__(self, app):
        self.app = app

    def run_load_and_validate(
        self,
        submissions: DataSubmissionRepository,
        submission_id: int,
        path: str,
        column_map: Dict[str, str],
    ):
        task_result = load_and_validate.apply_async(args=[path, column_map])
        report_dict = task_result.get()
        submissions.update_report(submission_id, report_dict)
        return report_from_dict(report_dict)
