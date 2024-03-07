import pytest
import re
from nad_ch.application.dtos import DataSubmissionReport, DataSubmissionReportOverview
from nad_ch.application.use_cases.data_producers import add_data_producer
from nad_ch.application.use_cases.data_submissions import (
    ingest_data_submission,
    list_data_submissions_by_producer,
    validate_data_submission,
)
from nad_ch.application.view_models import (
    DataSubmissionViewModel,
)
from nad_ch.config import create_app_context
from nad_ch.domain.repositories import DataSubmissionRepository


@pytest.fixture(scope="function")
def app_context():
    context = create_app_context()
    yield context


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
            self,
            submissions: DataSubmissionRepository,
            submission_id: int,
            path: str,
            config_name: str,
        ):
            return DataSubmissionReport(
                overview=DataSubmissionReportOverview(feature_count=1)
            )

    app_context._task_queue = CustomMockTestTaskQueue()
    config_name = "default"
    validate_data_submission(app_context, submission.filename, config_name)
    assert re.search(r"Total number of features: 1", caplog.text)
