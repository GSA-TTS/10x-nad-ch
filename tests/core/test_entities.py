import datetime
from nad_ch.core.entities import (
    DataProducer,
    DataSubmissionStatus,
    DataSubmission,
    ColumnMap,
    Role,
)


def test_data_submission_generates_file_path():
    producer = DataProducer("Some Producer")
    file_path = DataSubmission.generate_file_path("someupload.zip", producer)
    assert file_path == "someupload.zip"


def test_data_submission_generates_zipped_file_path():
    producer = DataProducer("Some Producer")
    file_path = DataSubmission.generate_zipped_file_path("someupload.zip", producer)
    assert file_path.startswith(
        "some_producer/"
    ), "String does not start with snakecase producer path"
    assert "someupload_zip" in file_path, "String does not contain snakecase filename"


def test_data_submission_knows_if_it_has_a_report():
    report_data = {"key1": "value1", "key2": "value2"}
    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, version_id=1)
    submission = DataSubmission(
        "MySubmission",
        "someupload.zip",
        DataSubmissionStatus.VALIDATED,
        producer,
        column_map,
        report_data,
    )
    assert submission.has_report()


def test_data_submission_knows_if_it_does_not_have_a_report():
    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, version_id=1)
    submission = DataSubmission(
        "MySubmission",
        "someupload.zip",
        DataSubmissionStatus.VALIDATED,
        producer,
        column_map,
    )
    assert not submission.has_report()


def test_column_map_is_valid():
    mapping = {
        "Add_Number": "address_number",
        "St_Name": "street_name",
        "St_PosTyp": "street_position_type",
        "Unit": "unit",
        "Inc_Muni": "city",
        "Post_City": "post_city",
        "DataSet_ID": "id",
    }

    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, mapping, 1)
    assert column_map.is_valid()


def test_column_map_is_invalid_if_missing_a_required_field():
    mapping = {
        "Add_Number": "address_number",
        "St_Name": "street_name",
        "St_PosTyp": "street_position_type",
        "Unit": "unit",
        "Inc_Muni": "city",
        "Post_City": "post_city",
        # "DataSet_ID": "id",
    }

    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, mapping, 1)
    assert not column_map.is_valid()


def test_column_map_is_invalid_if_empty():
    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, "{}", 1)
    assert not column_map.is_valid()


def test_column_map_is_invalid_if_empty_values_for_required_field():
    mapping = {
        "Add_Number": "address_number",
        "AddNo_Full": "address_number_full",
        "St_Name": "street_name",
        "StNam_Full": "street_name_full",
        "County": "county",
        "Inc_Muni": "city",
        "Post_City": "post_city",
        "State": "state",
        "UUID": "guid",
        "Longitude": "long",
        "Latitude": "lat",
        "NatGrid": "nat_grid",
        "AddrPoint": "address_point",
        "DateUpdate": "updated",
        "NAD_Source": "source",
        "DataSet_ID": "",
        "Placement": "placement",
        "AddAuth": "",
    }

    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, mapping, 1)
    assert not column_map.is_valid()


def test_role_has_permission():
    role = Role("admin", ["create", "read", "update", "delete"])
    assert role.has_permission("create")
    assert role.has_permission("read")
    assert role.has_permission("update")
    assert role.has_permission("delete")
