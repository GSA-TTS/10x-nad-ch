import os
from typing import List
from nad_ch.application.dtos import DownloadResult
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.application.view_models import (
    get_view_model,
    DataProviderViewModel,
    DataSubmissionViewModel,
)
from nad_ch.domain.entities import DataProvider, DataSubmission


def add_data_provider(
    ctx: ApplicationContext, provider_name: str
) -> DataProviderViewModel:
    if not provider_name:
        ctx.logger.error("Provider name required")
        return

    matching_provider = ctx.providers.get_by_name(provider_name)
    if matching_provider:
        ctx.logger.error("Provider name must be unique")
        return

    provider = DataProvider(provider_name)
    ctx.providers.add(provider)
    ctx.logger.info("Provider added")

    return get_view_model(provider)


def list_data_providers(ctx: ApplicationContext) -> List[DataProviderViewModel]:
    providers = ctx.providers.get_all()
    ctx.logger.info("Data Provider Names:")
    for p in providers:
        ctx.logger.info(p.name)

    return get_view_model(providers)


def ingest_data_submission(
    ctx: ApplicationContext, file_path: str, provider_name: str
) -> DataSubmissionViewModel:
    if not file_path:
        ctx.logger.error("File path required")
        return

    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() not in [".zip", ".csv"]:
        ctx.logger.error("Invalid file format. Only ZIP or CSV files are accepted.")
        return

    provider = ctx.providers.get_by_name(provider_name)
    if not provider:
        ctx.logger.error("Provider with that name does not exist")
        return

    try:
        filename = DataSubmission.generate_filename(file_path, provider)
        ctx.storage.upload(file_path, filename)

        submission = DataSubmission(filename, provider)
        ctx.submissions.add(submission)
        ctx.logger.info(f"Submission added: {submission.filename}")

        return get_view_model(submission)
    except Exception as e:
        ctx.storage.delete(filename)
        ctx.logger.error(f"Failed to process submission: {e}")


def get_data_submission(
    ctx: ApplicationContext, submission_id: int
) -> DataSubmissionViewModel:
    submission = ctx.submissions.get_by_id(submission_id)

    return get_view_model(submission)


def list_data_submissions_by_provider(
    ctx: ApplicationContext, provider_name: str
) -> List[DataSubmissionViewModel]:
    provider = ctx.providers.get_by_name(provider_name)
    if not provider:
        ctx.logger.error("Provider with that name does not exist")
        return

    submissions = ctx.submissions.get_by_provider(provider)
    ctx.logger.info(f"Data submissions for {provider.name}")
    for s in submissions:
        ctx.logger.info(f"{s.provider.name}: {s.filename}")

    return get_view_model(submissions)


def validate_data_submission(ctx: ApplicationContext, filename: str):
    submission = ctx.submissions.get_by_filename(filename)
    if not submission:
        ctx.logger.error("Data submission with that filename does not exist")
        return

    download_result: DownloadResult = ctx.storage.download_temp(filename)
    if not download_result:
        ctx.logger.error("Data extration error")
        return

    report = ctx.task_queue.run_load_and_validate(
        ctx.submissions, submission.id, download_result.extracted_dir
    )

    ctx.logger.info(f"Total number of features: {report.overview.feature_count}")

    ctx.storage.cleanup_temp_dir(download_result.temp_dir)
