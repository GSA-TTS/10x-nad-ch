import datetime
import json
from nad_ch.domain.entities import DataProducer, DataSubmission, ColumnMap


def test_data_submission_generates_filename():
    producer = DataProducer("Some Producer")
    filename = DataSubmission.generate_filename("someupload.zip", producer)
    todays_date = datetime.datetime.now().strftime("%Y%m%d")
    assert filename.startswith("some_producer_")
    assert todays_date in filename
    assert filename.endswith(".zip")


def test_data_submission_knows_if_it_has_a_report():
    report_data = {"key1": "value1", "key2": "value2"}
    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, version_id=1)
    submission = DataSubmission("someupload.zip", producer, column_map, report_data)
    assert submission.has_report()


def test_data_submission_knows_if_it_does_not_have_a_report():
    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, version_id=1)
    submission = DataSubmission("someupload.zip", producer, column_map)
    assert not submission.has_report()


def test_column_map_is_valid():
    mapping = {
        "GUID": "guid",
        "Source": "source",
        "LastUpdate": "last_update",
        "State": "state",
        "County": "county",
        "Zip_Code": "zip",
        "StreetName": "street",
        "Add_Number": "address_number",
        "Longitude": "longitude",
        "Latitude": "latitude",
        "NatGrid_Coord": "coord",
    }

    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, json.dumps(mapping), 1)
    assert column_map.is_valid()


def test_column_map_is_invalid_if_missing_a_required_field():
    mapping = {
        "GUID": "guid",
        "Source": "source",
        "LastUpdate": "last_update",
        "State": "state",
        "County": "county",
        "Zip_Code": "zip",
        "StreetName": "street",
        "Add_Number": "address_number",
        "Longitude": "longitude",
        "Latitude": "latitude",
    }

    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, json.dumps(mapping), 1)
    assert not column_map.is_valid()


def test_column_map_is_invalid_if_empty():
    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, "{}", 1)
    assert not column_map.is_valid()


def test_column_map_is_invalid_if_empty_values():
    mapping = {
        "GUID": "guid",
        "Source": "source",
        "LastUpdate": "last_update",
        "State": "state",
        "County": "county",
        "Zip_Code": "zip",
        "StreetName": "street",
        "Add_Number": "address_number",
        "Longitude": "longitude",
        "Latitude": "latitude",
        "NatGrid_Coord": "",
    }

    producer = DataProducer("Some producer")
    column_map = ColumnMap("TestMap", producer, json.dumps(mapping), 1)
    assert not column_map.is_valid()
