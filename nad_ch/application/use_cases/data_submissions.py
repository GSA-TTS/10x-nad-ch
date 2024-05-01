import os
from typing import List, IO
from nad_ch.application.dtos import DownloadResult
from nad_ch.application.exceptions import (
    InvalidDataSubmissionFileError,
    InvalidSchemaError,
)
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.application.validation import FileValidator
from nad_ch.application.view_models import (
    get_view_model,
    DataSubmissionViewModel,
)
from nad_ch.core.entities import DataSubmissionStatus, DataSubmission, ColumnMap
from nad_ch.config import LANDING_ZONE


def get_data_submission(
    ctx: ApplicationContext, submission_id: int
) -> DataSubmissionViewModel:
    submission = ctx.submissions.get_by_id(submission_id)

    if submission is None:
        return None

    return get_view_model(submission)


def get_data_submissions_by_producer(
    ctx: ApplicationContext, producer_name: str
) -> List[DataSubmissionViewModel]:
    producer = ctx.producers.get_by_name(producer_name)
    if not producer:
        ctx.logger.error("Producer with that name does not exist")
        return

    submissions = ctx.submissions.get_by_producer(producer)
    ctx.logger.info(f"Data submissions for {producer.name}")
    for s in submissions:
        ctx.logger.info(f"{s.producer.name}: {s.name}")

    return get_view_model(submissions)


def validate_data_submission(
    ctx: ApplicationContext, file_path: str, column_map_name: str
):
    submission = ctx.submissions.get_by_file_path(file_path)
    if not submission:
        ctx.logger.error("Data submission with that filename does not exist")
        return

    download_result: DownloadResult = ctx.storage.download_temp(file_path)
    if not download_result:
        ctx.logger.error("Data extration error")
        return

    column_map = ctx.column_maps.get_by_name_and_version(column_map_name, 1)
    if column_map is None:
        ctx.logger.error("Column map not found")
        return

    # Using version 1 for column maps for now, may add feature for user to select
    # version later
    try:
        mapped_data_local_dir = submission.get_mapped_data_dir(
            download_result.extracted_dir, LANDING_ZONE
        )
        mapped_data_remote_dir = submission.get_mapped_data_dir(
            download_result.extracted_dir, LANDING_ZONE, True
        )
        report = ctx.task_queue.run_load_and_validate(
            ctx.submissions,
            submission.id,
            download_result.extracted_dir,
            column_map.mapping,
            mapped_data_local_dir,
        )
        _ = ctx.task_queue.run_copy_mapped_data_to_remote(
            mapped_data_local_dir,
            mapped_data_remote_dir,
        )

        ctx.logger.info(f"Total number of features: {report.overview.feature_count}")
    except Exception:
        raise
    finally:
        ctx.storage.cleanup_temp_dir(download_result.temp_dir)
        ctx.storage.cleanup_temp_dir(mapped_data_local_dir)


def validate_file_before_submission(
    ctx: ApplicationContext, file: IO[bytes], column_map_id: int
) -> bool:
    column_map = ctx.column_maps.get_by_id(column_map_id)
    if column_map is None:
        raise ValueError("Column map not found")

    _, file_extension = os.path.splitext(file.filename)
    if file_extension.lower() != ".zip":
        raise InvalidDataSubmissionFileError(
            "Invalid file format. Only ZIP files are accepted."
        )

    file_validator = FileValidator(file, file.filename)
    print(file, file.name)
    if not file_validator.validate_file():
        raise InvalidDataSubmissionFileError(
            "Invalid zipped file. Only Shapefiles and Geodatabase files are accepted."
        )

    if not file_validator.validate_schema(column_map):
        raise InvalidSchemaError(
            "Invalid schema. The schema of the file must align with the schema of the \
            selected mapping."
        )

    return True


def create_data_submission(
    ctx: ApplicationContext,
    user_id: int,
    column_map_id: int,
    submission_name: str,
    file: IO[bytes],
):
    user = ctx.users.get_by_id(user_id)
    if user is None:
        raise ValueError("User not found")

    producer = user.producer
    if producer is None:
        raise ValueError("Producer not found")

    column_map = ctx.column_maps.get_by_id(column_map_id)
    if column_map is None:
        raise ValueError("Column map not found")

    try:
        file_path = DataSubmission.generate_zipped_file_path(submission_name, producer)
        submission = DataSubmission(
            submission_name,
            file_path,
            DataSubmissionStatus.PENDING_SUBMISSION,
            producer,
            column_map,
        )
        saved_submission = ctx.submissions.add(submission)

        ctx.storage.upload(file, file_path)

        ctx.logger.info(f"Submission added: {saved_submission.file_path}")

        return get_view_model(saved_submission)
    except Exception as e:
        ctx.storage.delete(file_path)
        ctx.logger.error(f"Failed to process submission: {e}")
