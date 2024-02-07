import pytest
import re
from nad_ch.application.dtos import DataSubmissionReport, DataSubmissionReportOverview
from nad_ch.config import create_app_context
from nad_ch.domain.entities import DataProvider, DataSubmission
from nad_ch.domain.repositories import DataSubmissionRepository
from nad_ch.application.use_cases import (
    add_data_provider,
    list_data_providers,
    ingest_data_submission,
    validate_data_submission,
)


@pytest.fixture(scope="function")
def app_context():
    context = create_app_context()
    yield context


def test_add_data_provider(app_context):
    name = "State X"
    add_data_provider(app_context, name)

    provider = app_context.providers.get_by_name(name)
    assert provider.name == name
    assert isinstance(provider, DataProvider) is True


def test_add_data_provider_logs_error_if_no_provider_name_given(mocker):
    mock_context = mocker.patch("nad_ch.config.create_app_context")
    add_data_provider(mock_context, "")
    mock_context.logger.error.assert_called_once_with("Provider name required")


def test_add_data_provider_logs_error_if_provider_name_not_unique(mocker):
    mock_context = mocker.patch("nad_ch.config.create_app_context")
    mock_context.providers.get_by_name.return_value("State X")
    add_data_provider(mock_context, "State X")

    mock_context.logger.error.assert_called_once_with("Provider name must be unique")


def test_list_a_single_data_provider(app_context):
    name = "State X"
    add_data_provider(app_context, name)

    providers = list_data_providers(app_context)

    assert len(providers) == 1
    assert providers[0].name == name


def test_list_multiple_data_providers(app_context):
    first_name = "State X"
    add_data_provider(app_context, first_name)

    second_name = "State Y"
    add_data_provider(app_context, second_name)

    providers = list_data_providers(app_context)
    assert len(providers) == 2
    assert providers[0].name == first_name
    assert providers[1].name == second_name


def test_ingest_data_submission(app_context):
    provider_name = "State X"
    add_data_provider(app_context, provider_name)

    filename = "my_cool_file.zip"
    ingest_data_submission(app_context, filename, provider_name)

    submission = app_context.submissions.get_by_id(1)
    assert isinstance(submission, DataSubmission) is True


def test_list_data_submissions_by_provider(app_context):
    provider_name = "State X"
    add_data_provider(app_context, provider_name)

    filename = "my_cool_file.zip"
    ingest_data_submission(app_context, filename, provider_name)

    provider = app_context.providers.get_by_name(provider_name)
    submissions = app_context.submissions.get_by_provider(provider)
    assert len(submissions) == 1


def test_validate_data_submission(app_context, caplog):
    provider_name = "State X"
    add_data_provider(app_context, provider_name)

    filename = "my_cool_file.zip"
    ingest_data_submission(app_context, filename, provider_name)
    submission = app_context.submissions.get_by_id(1)

    class CustomMockTestTaskQueue:
        def run_load_and_validate(
            self, submissions: DataSubmissionRepository, submission_id: int, path: str
        ):
            return DataSubmissionReport(
                overview=DataSubmissionReportOverview(feature_count=1)
            )

    app_context._task_queue = CustomMockTestTaskQueue()

    validate_data_submission(app_context, submission.filename)
    assert re.search(r"Total number of features: 1", caplog.text)
