import os
from nad_ch.application.data_handler import DataHandler
from conftest import TESTPRODUCER1_CONFIG, TESTPRODUCER2_CONFIG
import pickle
from pandas.testing import assert_frame_equal
import pytest

TEST_DATA_DIR = "tests/test_data"


def test_set_column_map(producer_column_maps):
    column_map_entity = producer_column_maps.get_by_name_and_version("testproducer1", 1)
    reader = DataHandler(column_map_entity.mapping)
    assert reader.column_map == TESTPRODUCER1_CONFIG

    column_map_entity = producer_column_maps.get_by_name_and_version("testproducer2", 1)
    reader = DataHandler(column_map_entity.mapping)
    assert reader.column_map == TESTPRODUCER2_CONFIG


def test_validate_column_map_duplicate_inputs(producer_column_maps):
    column_map_entity = producer_column_maps.get_by_name_and_version("testproducer4", 1)
    with pytest.raises(Exception) as exc:
        _ = DataHandler(column_map_entity.mapping)
    msg = "Duplicate inputs found for destination fields: COL_13 & COL_2, COL_5 & COL_6"
    assert str(exc.value) == msg


def test_read_file_in_batches_shape1(producer_column_maps):
    file_path = os.path.join(TEST_DATA_DIR, "shapefiles/usa-major-cities.zip")
    column_map_entity = producer_column_maps.get_by_name_and_version("testproducer2", 1)
    reader = DataHandler(column_map_entity.mapping)
    i = 0
    for gdf in reader.read_file_in_batches(path=file_path, batch_size=50):
        baseline_path = os.path.join(
            TEST_DATA_DIR,
            "shapefiles/baselines/test_read_file_in_batches_shape1/"
            f"usa-major-cities-gdf-{i}.pkl",
        )
        with open(baseline_path, "rb") as f:
            gdf_baseline = pickle.load(f)
        assert_frame_equal(gdf, gdf_baseline)
        i += 1


def test_read_file_in_batches_shape2(producer_column_maps):
    file_path = os.path.join(TEST_DATA_DIR, "shapefiles/NM911_Address_202310.zip")
    column_map_entity = producer_column_maps.get_by_name_and_version("testproducer3", 1)
    reader = DataHandler(column_map_entity.mapping)
    i = 0
    for gdf in reader.read_file_in_batches(path=file_path, batch_size=250):
        baseline_path = os.path.join(
            TEST_DATA_DIR,
            "shapefiles/baselines/test_read_file_in_batches_shape2/"
            f"NM911_Address_202310-gdf-{i}.pkl",
        )
        with open(baseline_path, "rb") as f:
            gdf_baseline = pickle.load(f)
        assert_frame_equal(gdf, gdf_baseline)
        i += 1


def test_read_file_in_batches_gdb1(producer_column_maps):
    file_path = os.path.join(TEST_DATA_DIR, "geodatabases/Naperville.gdb.zip")
    column_map_entity = producer_column_maps.get_by_name_and_version("testproducer1", 1)
    reader = DataHandler(column_map_entity.mapping)
    i = 0
    for gdf in reader.read_file_in_batches(path=file_path, batch_size=2000):
        baseline_path = os.path.join(
            TEST_DATA_DIR,
            "geodatabases/baselines/test_read_file_in_batches_gdb1/"
            f"naperville-gdf-{i}.pkl",
        )
        with open(baseline_path, "rb") as f:
            gdf_baseline = pickle.load(f)
        assert_frame_equal(gdf, gdf_baseline)
        i += 1
