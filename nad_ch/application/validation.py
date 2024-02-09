from typing import List
from geopandas import GeoDataFrame
from nad_ch.application.dtos import DataSubmissionReportFeature


def get_feature_count(gdf: GeoDataFrame) -> int:
    return len(gdf)


def get_feature_details(gdf: GeoDataFrame) -> List[DataSubmissionReportFeature]:
    report_features = []

    for column in gdf.columns:
        populated_count = gdf[column].notna().sum()
        null_count = gdf[column].isna().sum()

        report_feature = DataSubmissionReportFeature(
            provided_feature_name=column,
            nad_feature_name=column,
            populated_count=populated_count,
            null_count=null_count,
        )

        report_features.append(report_feature)

    return report_features
