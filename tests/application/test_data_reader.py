import os
from nad_ch.application.data_reader import DataReader
from tests.test_data.config_baselines import (
    EXPECTED_DEFAULT_CONFIG,
    TESTPROVIDER1_CONFIG,
    TESTPROVIDER2_CONFIG,
)
import pickle
from pandas.testing import assert_frame_equal
import pytest
from tests.fixtures import *

TEST_DATA_DIR = "tests/test_data"


def test_set_column_map(test_provider_column_maps):
    column_map_entity = test_provider_column_maps.get_by_name_and_version(
        "testprovider1", 1
    )
    reader = DataReader(column_map_entity.mapping)

    assert (
        reader.column_map["data_required_fields"]
        == EXPECTED_DEFAULT_CONFIG["data_required_fields"]
    )
    assert (
        reader.column_map["data_column_mapping"]
        != EXPECTED_DEFAULT_CONFIG["data_column_mapping"]
    )
    assert (
        reader.column_map["data_column_mapping"]
        == TESTPROVIDER1_CONFIG["data_column_mapping"]
    )

    column_map_entity = test_provider_column_maps.get_by_name_and_version(
        "testprovider2", 1
    )
    reader = DataReader(column_map_entity.mapping)

    assert (
        reader.column_map["data_required_fields"]
        == EXPECTED_DEFAULT_CONFIG["data_required_fields"]
    )
    assert (
        reader.column_map["data_column_mapping"]
        != EXPECTED_DEFAULT_CONFIG["data_column_mapping"]
    )
    assert (
        reader.column_map["data_column_mapping"]
        == TESTPROVIDER2_CONFIG["data_column_mapping"]
    )


def test_validate_column_map(test_provider_column_maps):
    column_map_entity = test_provider_column_maps.get_by_name_and_version(
        "testprovider1", 1
    )
    reader = DataReader(column_map_entity.mapping)
    with pytest.raises(Exception) as exc:
        reader.validate_column_map()
    msg = "Duplicate inputs found for destination fields: COL_13 & COL_2, COL_5 & COL_6"
    assert str(exc.value) == msg

    column_map_entity = test_provider_column_maps.get_by_name_and_version(
        "testprovider2", 1
    )
    reader = DataReader(column_map_entity.mapping)
    # No error raised
    reader.validate_column_map()


def test_read_file_in_batches_shape(test_provider_column_maps):
    file_path = os.path.join(
        TEST_DATA_DIR, "shapefiles/usa-major-cities/usa-major-cities.shp"
    )
    column_map_entity = test_provider_column_maps.get_by_name_and_version(
        "testprovider2", 1
    )
    reader = DataReader(column_map_entity.mapping)
    i = 0
    for gdf in reader.read_file_in_batches(path=file_path, batch_size=50):
        baseline_path = os.path.join(
            TEST_DATA_DIR, f"shapefiles/baselines/usa-major-cities-gdf-{i}.pkl"
        )
        with open(baseline_path, "rb") as f:
            gdf_baseline = pickle.load(f)
        assert_frame_equal(gdf, gdf_baseline)
        i += 1


def test_read_file_in_batches_gdb(test_provider_column_maps):
    file_path = os.path.join(TEST_DATA_DIR, "geodatabases/Naperville.gdb")
    column_map_entity = test_provider_column_maps.get_by_name_and_version(
        "testprovider1", 1
    )
    reader = DataReader(column_map_entity.mapping)
    i = 0
    for gdf in reader.read_file_in_batches(path=file_path, batch_size=2000):
        baseline_path = os.path.join(
            TEST_DATA_DIR, f"geodatabases/baselines/naperville-gdf-{i}.pkl"
        )
        with open(baseline_path, "rb") as f:
            gdf_baseline = pickle.load(f)
        assert_frame_equal(gdf, gdf_baseline)
        i += 1
