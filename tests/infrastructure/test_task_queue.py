import os
from nad_ch.infrastructure.task_queue import load_and_validate
from tests.application.test_data_reader import TEST_DATA_DIR
from conftest import NAPERVILLE_GDB_REPORT, MAJOR_CITIES_SHP_REPORT
import geopandas as gpd
import random
import numpy as np


def test_load_and_validate_testprovider1(
    celery_worker, celery_app, producer_column_maps
):
    column_map = producer_column_maps.get_by_name_and_version("testproducer1", 1)
    file_path = os.path.join(TEST_DATA_DIR, "geodatabases/Naperville.gdb")
    task_result = load_and_validate.delay(file_path, column_map.mapping)
    report_dict = task_result.get()
    assert report_dict == NAPERVILLE_GDB_REPORT


def test_load_and_validate_testprovider2(
    celery_worker, celery_app, producer_column_maps
):
    column_map = producer_column_maps.get_by_name_and_version("testproducer2", 1)
    file_path = os.path.join(
        TEST_DATA_DIR, "shapefiles/usa-major-cities/usa-major-cities.shp"
    )
    task_result = load_and_validate.delay(file_path, column_map.mapping)
    report_dict = task_result.get()
    assert report_dict == MAJOR_CITIES_SHP_REPORT
