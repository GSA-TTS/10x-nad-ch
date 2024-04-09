import os
import pickle
from geopandas import read_file
from pandas.testing import assert_frame_equal
from nad_ch.infrastructure.task_queue import (
    load_and_validate,
    copy_mapped_data_to_remote,
)
from tests.application.test_data_handler import TEST_DATA_DIR
from conftest import MAJOR_CITIES_SHP_REPORT, NM911_ADDRESS_202310_REPORT
import pytest


def test_load_and_validate_testprovider1(
    celery_worker, celery_app, producer_column_maps
):
    column_map = producer_column_maps.get_by_name_and_version("testproducer1", 1)
    file_path = os.path.join(TEST_DATA_DIR, "geodatabases/Naperville.gdb.zip")
    task_result = load_and_validate.delay(file_path, column_map.mapping, "")
    msg = "Duplicate inputs found for destination fields: COL_13 & COL_2, COL_5 & COL_6"
    with pytest.raises(Exception) as exc:
        _ = task_result.get()
        assert str(exc.value) == msg


def test_load_and_validate_testprovider2(
    celery_worker, celery_app, producer_column_maps, tmpdir
):
    column_map = producer_column_maps.get_by_name_and_version("testproducer2", 1)
    file_path = os.path.join(TEST_DATA_DIR, "shapefiles/usa-major-cities.zip")
    task_result = load_and_validate.delay(file_path, column_map.mapping, "")
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
    celery_worker, celery_app, producer_column_maps, tmpdir
):
    column_map = producer_column_maps.get_by_name_and_version("testproducer3", 1)
    file_path = os.path.join(TEST_DATA_DIR, "shapefiles/NM911_Address_202310.zip")
    temp_dir_path = tmpdir.mkdir("landing_zone")
    filename, _ = os.path.splitext(os.path.basename(file_path))
    mapped_data_dir = os.path.join(
        temp_dir_path,
        f"data_submissions/{column_map.producer.name}/1/{filename}",
    )
    mapped_data_path = os.path.join(mapped_data_dir, f"{filename}.zip")
    task_result = load_and_validate.delay(
        file_path, column_map.mapping, mapped_data_dir
    )
    report_dict = task_result.get()
    # Validate that mapped data was written to shape file correctly
    assert os.path.exists(mapped_data_path)
    baseline_path = os.path.join(
        TEST_DATA_DIR,
        "shapefiles/baselines/test_load_and_validate_testprovider3/"
        "NM911_Address_202310.pkl",
    )
    gdf = read_file(mapped_data_dir)
    with open(baseline_path, "rb") as f:
        gdf_baseline = pickle.load(f)
    assert_frame_equal(gdf, gdf_baseline)

    # Check that sorted values from missing required fields match
    assert sorted(report_dict["overview"]["missing_required_fields"]) == sorted(
        NM911_ADDRESS_202310_REPORT["overview"]["missing_required_fields"]
    )
    # Check all other values with missing required fields removed, since the list
    # order is not consistent between test runs
    del report_dict["overview"]["missing_required_fields"]
    del NM911_ADDRESS_202310_REPORT["overview"]["missing_required_fields"]
    assert report_dict == NM911_ADDRESS_202310_REPORT


def test_copy_mapped_data_to_remote(celery_worker, celery_app):
    mapped_data_local_dir = os.path.join(TEST_DATA_DIR, "shapefiles")
    mapped_data_remote_dir = (
        "data_submissions/Producer A/2024_04_02/NM911_Address_202310"
    )
    task_result = copy_mapped_data_to_remote.delay(
        mapped_data_local_dir,
        mapped_data_remote_dir,
    )
    result = task_result.get()
    assert result is True


@pytest.mark.skip(
    "Skipping to avoid build up of data in minio storage; "
    "this test is to ensure mapped data is uploaded to 'remote' "
    "storage successfully."
)
def test_copy_mapped_data_to_remote_2(celery_worker, celery_app, monkeypatch):
    # This test requires Minio to be running locally
    mapped_data_local_dir = os.path.join(TEST_DATA_DIR, "shapefiles")
    mapped_data_remote_dir = (
        "data_submissions/Producer A/2024_04_02/NM911_Address_202310"
    )
    monkeypatch.setenv("APP_ENV", "dev_local")
    task_result = copy_mapped_data_to_remote.delay(
        mapped_data_local_dir,
        mapped_data_remote_dir,
    )
    result = task_result.get()
    assert result is True
