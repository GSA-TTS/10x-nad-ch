import os
from typing import List
from nad_ch.application.dtos import DownloadResult
from nad_ch.application_context import ApplicationContext
from nad_ch.domain.entities import DataProvider, DataSubmission


def add_data_provider(ctx: ApplicationContext, provider_name: str) -> None:
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


def list_data_providers(ctx: ApplicationContext) -> List[DataProvider]:
    providers = ctx.providers.get_all()
    ctx.logger.info("Data Provider Names:")
    for p in providers:
        ctx.logger.info(p.name)

    return providers


def ingest_data_submission(
    ctx: ApplicationContext, file_path: str, provider_name: str
) -> None:
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
    except Exception as e:
        ctx.storage.delete(filename)
        ctx.logger.error(f"Failed to process submission: {e}")


def list_data_submissions_by_provider(
    ctx: ApplicationContext, provider_name: str
) -> List[DataSubmission]:
    provider = ctx.providers.get_by_name(provider_name)
    if not provider:
        ctx.logger.error("Provider with that name does not exist")
        return

    submissions = ctx.submissions.get_by_provider(provider)
    ctx.logger.info(f"Data submissions for {provider.name}")
    for s in submissions:
        ctx.logger.info(f"{s.provider.name}: {s.filename}")

    return submissions


def validate_data_submission(ctx: ApplicationContext, filename: str):
    submission = ctx.submissions.get_by_filename(filename)
    if not submission:
        ctx.logger.error("Data submission with that filename does not exist")
        return

    download_result: DownloadResult = ctx.storage.download_temp(filename)
    if not download_result:
        ctx.logger.error("Data extration error")
        return

    result = ctx.task_queue.run_load_and_validate(download_result.extracted_dir)

    ctx.logger.info(f"Total number of features: {result.get()}")

    ctx.storage.cleanup_temp_dir(download_result.temp_dir)
