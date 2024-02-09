import geopandas as gpd
from shapely.geometry import Polygon
from nad_ch.application.dtos import DataSubmissionReportFeature
from nad_ch.application.validation import get_feature_count, get_feature_details
from tests.factories import create_fake_geopandas_dataframe


def test_get_feature_count_finds_the_length_of_a_geopandas_dataframe():
    coordinates = [(0, 0), (0, 1), (1, 1), (1, 0)]
    polygon = Polygon(coordinates)
    gdf = gpd.GeoDataFrame(geometry=[polygon])
    assert (get_feature_count(gdf)) == 1


def test_get_feature_details_returns_instances_of_correct_dataclass():
    gdf = create_fake_geopandas_dataframe(num_rows=1)
    feature_details = get_feature_details(gdf)
    feature = feature_details[0]
    assert isinstance(feature, DataSubmissionReportFeature)
