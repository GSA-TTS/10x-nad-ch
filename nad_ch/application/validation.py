from typing import Dict, Tuple
from geopandas import GeoDataFrame
from nad_ch.application.dtos import (
    DataSubmissionReportFeature,
    DataSubmissionReportOverview,
)


def get_feature_count(gdf: GeoDataFrame) -> int:
    return len(gdf.columns)


def get_record_count(gdf: GeoDataFrame, null_rows_only: bool = False) -> int:
    if null_rows_only:
        return len(gdf[gdf.isnull().any(axis=1)])
    return len(gdf)


def get_features_flagged(features: Dict[str, DataSubmissionReportFeature]) -> int:
    return len(
        [k for k, v in features.items() if v.null_count + v.invalid_domain_count > 0]
    )


def initialize_overview_details(
    gdf: GeoDataFrame, column_maps: Dict[str, str]
) -> Tuple[DataSubmissionReportOverview, Dict[str, DataSubmissionReportFeature]]:
    report_overview = DataSubmissionReportOverview(feature_count=get_feature_count(gdf))
    report_features = {
        nad_name: DataSubmissionReportFeature(
            provided_feature_name=provided_name, nad_feature_name=nad_name
        )
        for provided_name, nad_name in column_maps.items()
    }
    return report_overview, report_features


def update_feature_details(
    gdf: GeoDataFrame, features: Dict[str, DataSubmissionReportFeature]
) -> Dict[str, DataSubmissionReportFeature]:
    for column in gdf.columns:
        populated_count = gdf[column].notna().sum()
        null_count = gdf[column].isna().sum()

        feature_submission = features.get(column)
        if feature_submission:
            feature_submission.populated_count += populated_count
            feature_submission.null_count += null_count
            # TODO: Add logic for domain specific features such as
            # valid_domain_count, invalid_domain_count, & invalid_domains
    return features


def update_overview_details(
    gdf: GeoDataFrame, overview: DataSubmissionReportOverview
) -> DataSubmissionReportOverview:
    overview.records_count += get_record_count(gdf)
    overview.records_flagged += get_record_count(gdf, True)
    return overview


def finalize_overview_details(
    features: Dict[str, DataSubmissionReportFeature],
    overview: DataSubmissionReportOverview,
) -> DataSubmissionReportOverview:
    overview.features_flagged += get_features_flagged(features)
    # TODO: Add logic for etl_update_required & data_update_required
    return overview
