import os
from typing import List
from nad_ch.application.dtos import DownloadResult
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.application.view_models import (
    get_view_model,
    DataSubmissionViewModel,
)
from nad_ch.domain.entities import DataSubmission, ColumnMap


def ingest_data_submission(
    ctx: ApplicationContext, file_path: str, producer_name: str
) -> DataSubmissionViewModel:
    if not file_path:
        ctx.logger.error("File path required")
        return

    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() not in [".zip", ".csv"]:
        ctx.logger.error("Invalid file format. Only ZIP or CSV files are accepted.")
        return

    producer = ctx.producers.get_by_name(producer_name)
    if not producer:
        ctx.logger.error("Producer with that name does not exist")
        return

    try:
        filename = DataSubmission.generate_filename(file_path, producer)
        ctx.storage.upload(file_path, filename)

        # TODO: Finish logic for obtaining column map from user
        column_map = ColumnMap("placeholder", producer, 1)

        submission = DataSubmission(filename, producer, column_map)
        saved_submission = ctx.submissions.add(submission)
        ctx.logger.info(f"Submission added: {saved_submission.filename}")

        return get_view_model(saved_submission)
    except Exception as e:
        ctx.storage.delete(filename)
        ctx.logger.error(f"Failed to process submission: {e}")


def get_data_submission(
    ctx: ApplicationContext, submission_id: int
) -> DataSubmissionViewModel:
    submission = ctx.submissions.get_by_id(submission_id)

    if submission is None:
        return None

    return get_view_model(submission)


def list_data_submissions_by_producer(
    ctx: ApplicationContext, producer_name: str
) -> List[DataSubmissionViewModel]:
    producer = ctx.producers.get_by_name(producer_name)
    if not producer:
        ctx.logger.error("Producer with that name does not exist")
        return

    submissions = ctx.submissions.get_by_producer(producer)
    ctx.logger.info(f"Data submissions for {producer.name}")
    for s in submissions:
        ctx.logger.info(f"{s.producer.name}: {s.filename}")

    return get_view_model(submissions)


def validate_data_submission(
    ctx: ApplicationContext, filename: str, column_map_name: str
):
    submission = ctx.submissions.get_by_filename(filename)
    if not submission:
        ctx.logger.error("Data submission with that filename does not exist")
        return

    download_result: DownloadResult = ctx.storage.download_temp(filename)
    if not download_result:
        ctx.logger.error("Data extration error")
        return

    # Using version 1 for column maps for now, may add feature for user to select
    # version later
    column_map = ctx.column_maps.get_by_name_and_version(column_map_name, 1)
    report = ctx.task_queue.run_load_and_validate(
        ctx.submissions,
        submission.id,
        download_result.extracted_dir,
        column_map.mapping,
    )

    ctx.logger.info(f"Total number of features: {report.overview.feature_count}")

    ctx.storage.cleanup_temp_dir(download_result.temp_dir)
