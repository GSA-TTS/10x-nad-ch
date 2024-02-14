import pytest
import re
from nad_ch.application.dtos import DataSubmissionReport, DataSubmissionReportOverview
from nad_ch.application.use_cases import (
    add_data_producer,
    list_data_producers,
    ingest_data_submission,
    list_data_submissions_by_producer,
    validate_data_submission,
)
from nad_ch.application.view_models import (
    DataProducerViewModel,
    DataSubmissionViewModel,
)
from nad_ch.config import create_app_context
from nad_ch.domain.repositories import DataSubmissionRepository


@pytest.fixture(scope="function")
def app_context():
    context = create_app_context()
    yield context


def is_valid_date_format(date_str: str) -> bool:
    """
    Verify that a given string matches the following format:
    'January 1, 2024'
    """
    pattern = r"^\w+\s+\d{2},\s+\d{4}$"
    match = re.match(pattern, date_str)
    return bool(match)


def test_add_data_producer(app_context):
    name = "State X"

    result = add_data_producer(app_context, name)

    assert isinstance(result, DataProducerViewModel)
    assert is_valid_date_format(result.date_created)


def test_add_data_producer_logs_error_if_no_producer_name_given(mocker):
    mock_context = mocker.patch("nad_ch.config.create_app_context")
    add_data_producer(mock_context, "")
    mock_context.logger.error.assert_called_once_with("Producer name required")


def test_add_data_producer_logs_error_if_producer_name_not_unique(mocker):
    mock_context = mocker.patch("nad_ch.config.create_app_context")
    mock_context.producer.get_by_name.return_value("State X")
    add_data_producer(mock_context, "State X")

    mock_context.logger.error.assert_called_once_with("Producer name must be unique")


def test_list_a_single_data_producer(app_context):
    name = "State X"
    add_data_producer(app_context, name)

    result = list_data_producers(app_context)

    assert len(result) == 1
    assert isinstance(result[0], DataProducerViewModel)
    assert result[0].name == name


def test_list_multiple_data_producers(app_context):
    first_name = "State X"
    add_data_producer(app_context, first_name)

    second_name = "State Y"
    add_data_producer(app_context, second_name)

    result = list_data_producers(app_context)
    assert len(result) == 2
    assert isinstance(result[0], DataProducerViewModel)
    assert result[0].name == first_name
    assert isinstance(result[1], DataProducerViewModel)
    assert result[1].name == second_name


def test_ingest_data_submission(app_context):
    producer_name = "State X"
    add_data_producer(app_context, producer_name)

    filename = "my_cool_file.zip"

    result = ingest_data_submission(app_context, filename, producer_name)

    assert isinstance(result, DataSubmissionViewModel)


def test_list_data_submissions_by_producer(app_context):
    producer_name = "State X"
    add_data_producer(app_context, producer_name)

    filename = "my_cool_file.zip"
    ingest_data_submission(app_context, filename, producer_name)

    result = list_data_submissions_by_producer(app_context, producer_name)

    assert len(result) == 1
    assert isinstance(result[0], DataSubmissionViewModel)


def test_validate_data_submission(app_context, caplog):
    producer_name = "State X"
    add_data_producer(app_context, producer_name)

    filename = "my_cool_file.zip"
    ingest_data_submission(app_context, filename, producer_name)
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
