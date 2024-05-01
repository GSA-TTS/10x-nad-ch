import pytest
import re
from nad_ch.application.dtos import DataSubmissionReport, DataSubmissionReportOverview
from nad_ch.application.use_cases.data_producers import add_data_producer
from nad_ch.application.use_cases.data_submissions import (
    get_data_submission,
    get_data_submissions_by_producer,
    validate_data_submission,
    validate_file_before_submission,
    create_data_submission,
)
from nad_ch.application.view_models import (
    DataSubmissionViewModel,
)
from nad_ch.config import create_app_context
from nad_ch.core.entities import ColumnMap, DataProducer, User
from nad_ch.core.repositories import DataSubmissionRepository
from typing import Dict


@pytest.fixture(scope="function")
def app_context():
    context = create_app_context()
    yield context


def test_get_data_submission(app_context):
    producer_name = "New Jersey"
    nj = app_context.producers.add(DataProducer(producer_name))
    user = app_context.users.add(User("test@test.org", "foo", "bar", True, nj))
    column_map = app_context.column_maps.add(
        ColumnMap(
            "TestMap",
            nj,
            {
                "Add_Number": "address_number",
                "St_Name": "street_name",
                "St_PosTyp": "street_position_type",
                "Unit": "unit",
                "Inc_Muni": "city",
                "Post_City": "post_city",
                "DataSet_ID": "id",
            },
        )
    )
    submission = create_data_submission(
        app_context, user.id, column_map.id, "TestSubmission", "test.zip"
    )

    result = get_data_submission(app_context, submission.id)

    assert isinstance(result, DataSubmissionViewModel)


def test_get_data_submissions_by_producer(app_context):
    producer_name = "New Jersey"
    nj = app_context.producers.add(DataProducer(producer_name))
    user = app_context.users.add(User("test@test.org", "foo", "bar", True, nj))
    column_map = app_context.column_maps.add(
        ColumnMap(
            "TestMap",
            nj,
            {
                "Add_Number": "address_number",
                "St_Name": "street_name",
                "St_PosTyp": "street_position_type",
                "Unit": "unit",
                "Inc_Muni": "city",
                "Post_City": "post_city",
                "DataSet_ID": "id",
            },
        )
    )
    create_data_submission(
        app_context, user.id, column_map.id, "TestSubmission", "test.zip"
    )

    result = get_data_submissions_by_producer(app_context, producer_name)

    assert len(result) == 1
    assert isinstance(result[0], DataSubmissionViewModel)


def test_create_data_submission(app_context):
    nj = app_context.producers.add(DataProducer("New Jersey"))
    user = app_context.users.add(User("test@test.org", "foo", "bar", True, nj))
    column_map = app_context.column_maps.add(
        ColumnMap(
            "TestMap",
            nj,
            {
                "Add_Number": "address_number",
                "St_Name": "street_name",
                "St_PosTyp": "street_position_type",
                "Unit": "unit",
                "Inc_Muni": "city",
                "Post_City": "post_city",
                "DataSet_ID": "id",
            },
        )
    )
    result = create_data_submission(
        app_context, user.id, column_map.id, "TestSubmission", "test.zip"
    )

    assert isinstance(result, DataSubmissionViewModel)


def test_validate_data_submission(app_context, caplog):
    producer_name = "New Jersey"
    nj = app_context.producers.add(DataProducer(producer_name))
    user = app_context.users.add(User("test@test.org", "foo", "bar", True, nj))
    column_map_name = "TestMap"
    column_map = app_context.column_maps.add(
        ColumnMap(
            column_map_name,
            nj,
            {
                "Add_Number": "address_number",
                "St_Name": "street_name",
                "St_PosTyp": "street_position_type",
                "Unit": "unit",
                "Inc_Muni": "city",
                "Post_City": "post_city",
                "DataSet_ID": "id",
            },
            1,
        )
    )

    vm = create_data_submission(
        app_context, user.id, column_map.id, "TestSubmission", "test.zip"
    )
    submission = app_context.submissions.get_by_id(vm.id)

    class CustomMockTestTaskQueue:
        def run_load_and_validate(
            self,
            submissions: DataSubmissionRepository,
            submission_id: int,
            path: str,
            column_map: Dict[str, str],
            mapped_data_dir: str,
        ):
            return DataSubmissionReport(
                overview=DataSubmissionReportOverview(feature_count=1)
            )

        def run_copy_mapped_data_to_remote(
            self, mapped_data_local_dir: str, mapped_data_remote_dir: str
        ):

            return True

    app_context._task_queue = CustomMockTestTaskQueue()

    validate_data_submission(app_context, submission.file_path, column_map_name)

    assert re.search(r"Total number of features: 1", caplog.text)
