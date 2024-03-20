import os
from nad_ch.infrastructure.task_queue import load_and_validate
from tests.application.test_data_reader import TEST_DATA_DIR
from conftest import MAJOR_CITIES_SHP_REPORT, NM911_ADDRESS_202310_REPORT
import pytest


def test_load_and_validate_testprovider1(
    celery_worker, celery_app, producer_column_maps
):
    column_map = producer_column_maps.get_by_name_and_version("testproducer1", 1)
    file_path = os.path.join(TEST_DATA_DIR, "geodatabases/Naperville.gdb")
    task_result = load_and_validate.delay(file_path, column_map.mapping)
    msg = "Duplicate inputs found for destination fields: COL_13 & COL_2, COL_5 & COL_6"
    with pytest.raises(Exception) as exc:
        _ = task_result.get()
        assert str(exc.value) == msg


def test_load_and_validate_testprovider2(
    celery_worker, celery_app, producer_column_maps
):
    column_map = producer_column_maps.get_by_name_and_version("testproducer2", 1)
    file_path = os.path.join(
        TEST_DATA_DIR, "shapefiles/usa-major-cities/usa-major-cities.shp"
    )
    task_result = load_and_validate.delay(file_path, column_map.mapping)
    report_dict = task_result.get()
    # Check that sorted values from missing required fields match
    assert sorted(report_dict["overview"]["missing_required_fields"]) == sorted(
        MAJOR_CITIES_SHP_REPORT["overview"]["missing_required_fields"]
    )
    # Check all other values with missing required fields removed, since the list
    # order is not consistent between test runs
    del report_dict["overview"]["missing_required_fields"]
    del MAJOR_CITIES_SHP_REPORT["overview"]["missing_required_fields"]
    assert report_dict == MAJOR_CITIES_SHP_REPORT


def test_load_and_validate_testprovider3(
    celery_worker, celery_app, producer_column_maps
):
    column_map = producer_column_maps.get_by_name_and_version("testproducer3", 1)
    file_path = os.path.join(
        TEST_DATA_DIR, "shapefiles/NM911_Address_202310/NM911_Address_202310.shp"
    )
    task_result = load_and_validate.delay(file_path, column_map.mapping)
    report_dict = task_result.get()
    # Check that sorted values from missing required fields match
    assert sorted(report_dict["overview"]["missing_required_fields"]) == sorted(
        NM911_ADDRESS_202310_REPORT["overview"]["missing_required_fields"]
    )
    # Check all other values with missing required fields removed, since the list
    # order is not consistent between test runs
    del report_dict["overview"]["missing_required_fields"]
    del NM911_ADDRESS_202310_REPORT["overview"]["missing_required_fields"]
    assert report_dict == NM911_ADDRESS_202310_REPORT
