import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from nad_ch.application.validation import get_feature_count


def test_get_feature_count():
    coordinates = [(0, 0), (0, 1), (1, 1), (1, 0)]
    polygon = Polygon(coordinates)
    gdf = gpd.GeoDataFrame(geometry=[polygon])
    assert (get_feature_count(gdf)) == 1
