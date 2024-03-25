import geopandas as gpd
from shapely.geometry import Polygon
from nad_ch.application.dtos import (
    DataSubmissionReportFeature,
    DataSubmissionReportOverview,
)
from nad_ch.application.validation import DataValidator
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
    assert DataValidator.get_feature_count(gdf) == 1


def test_get_record_count():
    gdf = create_fake_geopandas_dataframe(num_rows=2)
    assert DataValidator.get_record_count(gdf) == 2


def test_get_features_flagged_count():
    gdf = create_fake_geopandas_dataframe()
    column_map = create_fake_column_map_from_gdf(gdf)
    data_validator = DataValidator(column_map)
    data_validator.initialize_overview_details(gdf, column_map)
    data_validator.report_features["St_Name"].null_count = 2
    data_validator.report_features["Floor"].invalid_domain_count = 7
    assert data_validator.get_features_flagged(data_validator.report_features) == 2


def test_load_domain_values():
    gdf = create_fake_geopandas_dataframe(num_rows=10)
    column_map = create_fake_column_map_from_gdf(gdf)
    data_validator = DataValidator(column_map)
    domains = data_validator.domains
    domain_specific_fields = (
        "County",
        "Placement",
        "St_PosDir",
        "St_PosTyp",
        "St_PreDir",
        "St_PreSep",
        "St_PreTyp",
        "State",
    )
    domain_keys = ("domain", "mapper")
    assert all(key in domains.keys() for key in domain_keys)
    assert all(field in domains["domain"] for field in domain_specific_fields)
    assert all(field in domains["mapper"] for field in domain_specific_fields)


def test_update_feature_details():
    gdf = create_fake_geopandas_dataframe(num_rows=10)
    column_map = create_fake_column_map_from_gdf(gdf)
    data_validator = DataValidator(column_map)
    data_validator.initialize_overview_details(gdf, column_map)
    data_validator.update_feature_details(gdf)
    assert isinstance(
        data_validator.report_features.get("AddNum_Pre"), DataSubmissionReportFeature
    )
    # Null count assertions
    for nad_field in column_map.values():
        feature = data_validator.report_features.get(nad_field)
        if feature.nad_feature_name in NULL_NAD_FIELDS:
            assert feature.populated_count == 0
            assert feature.null_count == 10
        else:
            assert feature.populated_count == 10
            assert feature.null_count == 0

    # Invalid Domain assertions
    feature = data_validator.report_features.get("County")
    assert feature.invalid_domain_count == 10
    assert feature.valid_domain_count == 0
    assert feature.invalid_domains == ["Anycounty"]


def test_initialize_overview_details():
    gdf = create_fake_geopandas_dataframe(num_rows=1)
    column_map = create_fake_column_map_from_gdf(gdf)
    data_validator = DataValidator(column_map)
    data_validator.initialize_overview_details(gdf, column_map)
    overview_attributes_to_check = [
        attr
        for attr in data_validator.report_overview.__annotations__.keys()
        if attr not in ("feature_count", "missing_required_fields")
    ]

    assert isinstance(data_validator.report_overview, DataSubmissionReportOverview)
    assert data_validator.report_overview.feature_count == 36
    assert data_validator.report_overview.missing_required_fields == [
        "NatGrid",
        "AddrPoint",
    ]
    assert all(
        getattr(data_validator.report_overview, attribute) == 0
        for attribute in overview_attributes_to_check
    )

    assert isinstance(
        data_validator.report_features.get("St_Name"), DataSubmissionReportFeature
    )
    assert all(
        feature.nad_feature_name in gdf.columns
        for _, feature in data_validator.report_features.items()
    )


def test_update_overview_details():
    gdf = create_fake_geopandas_dataframe(num_rows=5)
    column_map = create_fake_column_map_from_gdf(gdf)
    data_validator = DataValidator(column_map)
    data_validator.initialize_overview_details(gdf, column_map)
    data_validator.update_overview_details(gdf)
    assert data_validator.report_overview.records_count == 5
    assert data_validator.report_overview.records_flagged == 5

    gdf = gdf[[col for col in gdf.columns if col not in NULL_NAD_FIELDS]]
    column_map = create_fake_column_map_from_gdf(gdf)
    data_validator = DataValidator(column_map)
    data_validator.initialize_overview_details(gdf, column_map)
    data_validator.update_overview_details(gdf)
    assert data_validator.report_overview.records_count == 5
    assert data_validator.report_overview.records_flagged == 0


def test_finalize_overview_details():
    gdf = create_fake_geopandas_dataframe()
    column_map = create_fake_column_map_from_gdf(gdf)
    data_validator = DataValidator(column_map)
    data_validator.initialize_overview_details(gdf, column_map)
    data_validator.report_features["St_Name"].null_count = 2
    data_validator.report_features["Floor"].invalid_domain_count = 7
    data_validator.finalize_overview_details()
    assert data_validator.report_overview.features_flagged == 2
