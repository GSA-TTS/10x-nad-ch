import os
from nad_ch.config.development_local import (
    DevLocalApplicationContext as dev_local_app_context,
)
from nad_ch.config.development_remote import (
    DevRemoteApplicationContext as dev_remote_app_context,
)
from nad_ch.config.test import TestApplicationContext as test_app_context
from celery import Celery
from nad_ch.application.dtos import (
    DataSubmissionReport,
    report_to_dict,
    report_from_dict,
)
from nad_ch.application.data_handler import DataHandler
from nad_ch.application.interfaces import TaskQueue
from nad_ch.application.validation import DataValidator
from nad_ch.config import QUEUE_BROKER_URL, QUEUE_BACKEND_URL
from nad_ch.core.repositories import DataSubmissionRepository
from datetime import datetime, timezone
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
    task_concurrency=4,
    store_processed=True,
    result_persistent=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)


@celery_app.task(bind=True, max_retries=2)
def load_and_validate(
    self, gdb_file_path: str, column_map: Dict[str, str], mapped_data_dir: str
) -> dict:
    try:
        data_handler = DataHandler(column_map, mapped_data_dir)
        first_batch = True
        for gdf in data_handler.read_file_in_batches(path=gdb_file_path):
            if first_batch:
                data_validator = DataValidator(data_handler.valid_renames)
            data_validator.run(gdf)
            first_batch = False
        data_validator.finalize_overview_details()
        report = DataSubmissionReport(
            data_validator.report_overview,
            list(data_validator.report_features.values()),
        )
    except Exception as e:
        raise self.retry(exec=e, countdown=30)
    return report_to_dict(report)


@celery_app.task(bind=True, max_retries=2)
def copy_mapped_data_to_remote(
    self, mapped_data_local_dir: str, mapped_data_remote_dir: str
) -> bool:
    try:
        success = True
        app_context = TaskHelperFunctions.get_app_context()
        storage_interface = app_context.create_storage()
        filename = mapped_data_remote_dir.split("/")[-1]
        timestamp = datetime.now(timezone.utc).strftime("%Y_%m_%d_%H%M%S")
        # Copy mapped dataset to remote storage
        storage_interface.upload(
            os.path.join(mapped_data_local_dir, f"{filename}.zip"),
            os.path.join(mapped_data_remote_dir, f"{filename}_{timestamp}.zip"),
        )
    except Exception as e:
        raise self.retry(exec=e, countdown=30)
    return success


class CeleryTaskQueue(TaskQueue):
    def __init__(self, app):
        self.app = app

    def run_load_and_validate(
        self,
        submissions: DataSubmissionRepository,
        submission_id: int,
        path: str,
        column_map: Dict[str, str],
        mapped_data_dir: str,
    ):
        task_result = load_and_validate.apply_async(
            args=[path, column_map, mapped_data_dir]
        )
        report_dict = task_result.get()
        submissions.update_report(submission_id, report_dict)
        return report_from_dict(report_dict)

    def run_copy_mapped_data_to_remote(
        self,
        mapped_data_dir: str,
        mapped_data_remote_dir: str,
    ):
        task_result = copy_mapped_data_to_remote.apply_async(
            args=[mapped_data_dir, mapped_data_remote_dir]
        )
        success = task_result.get()
        return success


class TaskHelperFunctions:

    @staticmethod
    def get_app_context():
        APP_ENV = os.environ.get("APP_ENV")
        if APP_ENV == "dev_local":
            app_context = dev_local_app_context
        elif APP_ENV == "dev_remote":
            app_context = dev_remote_app_context
        elif APP_ENV == "test":
            app_context = test_app_context
        return app_context
