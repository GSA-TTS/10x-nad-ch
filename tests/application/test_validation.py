from typing import Dict
import geopandas as gpd
from shapely.geometry import Polygon
from nad_ch.application.dtos import (
    DataSubmissionReportFeature,
    DataSubmissionReportOverview,
)
from nad_ch.application.validation import (
    get_feature_count,
    get_record_count,
    get_features_flagged,
    update_feature_details,
    initialize_overview_details,
    update_overview_details,
    finalize_overview_details,
)
from tests.factories import (
    create_fake_geopandas_dataframe,
    create_fake_column_map_from_gdf,
)

NULL_NAD_FIELDS = [
    "AddNum_Pre",
    "AddNum_Suf",
    "St_PreMod",
    "St_PreTyp",
    "St_PreSep",
    "St_PosDir",
    "St_PosMod",
    "Building",
    "Floor",
    "Unit",
    "Room",
    "Seat",
    "Addtl_Loc",
    "SubAddress",
    "LandmkName",
]


def test_get_feature_count_finds_the_header_length_of_a_geopandas_dataframe():
    coordinates = [(0, 0), (0, 1), (1, 1), (1, 0)]
    polygon = Polygon(coordinates)
    gdf = gpd.GeoDataFrame(geometry=[polygon])
    assert get_feature_count(gdf) == 1


def test_get_record_count():
    gdf = create_fake_geopandas_dataframe(num_rows=2)
    assert get_record_count(gdf) == 2


def test_get_features_flagged_count():
    gdf = create_fake_geopandas_dataframe()
    column_maps = create_fake_column_map_from_gdf(gdf)
    _, features = initialize_overview_details(gdf, column_maps)
    features["St_Name"].null_count = 2
    features["Floor"].invalid_domain_count = 7
    assert get_features_flagged(features) == 2


def test_update_feature_details():
    gdf = create_fake_geopandas_dataframe(num_rows=10)
    column_maps = create_fake_column_map_from_gdf(gdf)
    _, features = initialize_overview_details(gdf, column_maps)
    feature_details = update_feature_details(gdf, features)
    assert isinstance(feature_details.get("AddNum_Pre"), DataSubmissionReportFeature)
    for nad_field in column_maps.values():
        feature = feature_details.get(nad_field)
        if feature.nad_feature_name in NULL_NAD_FIELDS:
            assert feature.populated_count == 0
            assert feature.null_count == 10
        elif (
            feature.nad_feature_name not in NULL_NAD_FIELDS
            and feature.nad_feature_name not in gdf.columns
        ):
            print(feature.nad_feature_name)
        else:
            assert feature.populated_count == 10
            assert feature.null_count == 0
        # TODO: Add assertions for invalid domain metrics


def test_initialize_overview_details():
    gdf = create_fake_geopandas_dataframe(num_rows=1)
    column_maps = create_fake_column_map_from_gdf(gdf)
    overview, features = initialize_overview_details(gdf, column_maps)
    overview_attributes_to_check = [
        attr for attr in overview.__annotations__.keys() if attr != "feature_count"
    ]

    assert isinstance(overview, DataSubmissionReportOverview)
    assert overview.feature_count == 36
    assert all(
        getattr(overview, attribute) == 0 for attribute in overview_attributes_to_check
    )

    assert isinstance(features.get("St_Name"), DataSubmissionReportFeature)
    assert all(
        feature.nad_feature_name in gdf.columns for _, feature in features.items()
    )


def test_update_overview_details():
    gdf = create_fake_geopandas_dataframe(num_rows=5)
    column_maps = create_fake_column_map_from_gdf(gdf)
    overview, _ = initialize_overview_details(gdf, column_maps)
    overview = update_overview_details(gdf, overview)
    assert overview.records_count == 5
    assert overview.records_flagged == 5

    gdf = gdf[[col for col in gdf.columns if col not in NULL_NAD_FIELDS]]
    overview, _ = initialize_overview_details(gdf, column_maps)
    overview = update_overview_details(gdf, overview)
    assert overview.records_count == 5
    assert overview.records_flagged == 0


def test_finalize_overview_details():
    gdf = create_fake_geopandas_dataframe()
    column_maps = create_fake_column_map_from_gdf(gdf)
    overview, features = initialize_overview_details(gdf, column_maps)
    features["St_Name"].null_count = 2
    features["Floor"].invalid_domain_count = 7
    overview = finalize_overview_details(overview, features)
    assert overview.features_flagged == 2
