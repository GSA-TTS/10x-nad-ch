import numpy as np
from nad_ch.application.dtos import (
    DataSubmissionReport,
    DataSubmissionReportOverview,
    DataSubmissionReportFeature,
    report_to_dict,
    report_from_dict,
)


def test_to_dict_simple():
    overview = DataSubmissionReportOverview(feature_count=100, features_flagged=5)

    overview_dict = report_to_dict(overview)

    assert overview_dict == {
        "feature_count": 100,
        "features_flagged": 5,
        "etl_update_required": False,
        "data_update_required": False,
    }


def test_to_dict_with_numpy_types():
    feature = DataSubmissionReportFeature(
        provided_feature_name="id",
        nad_feature_name="id",
        populated_count=np.int64(100),
        null_count=np.float32(0),
    )

    feature_dict = report_to_dict(feature)

    assert feature_dict == {
        "provided_feature_name": "id",
        "nad_feature_name": "id",
        "populated_count": 100,
        "null_count": 0,
    }
    assert isinstance(feature_dict["populated_count"], int)
    assert isinstance(feature_dict["null_count"], float)


def test_from_dict_to_dataclass():
    report_dict = {
        "overview": {
            "feature_count": 100,
            "features_flagged": 5,
            "etl_update_required": False,
            "data_update_required": False,
        },
        "features": [
            {
                "provided_feature_name": "id",
                "nad_feature_name": "id",
                "populated_count": 100,
                "null_count": 0,
            }
        ],
    }

    report = report_from_dict(report_dict)

    assert report.overview.feature_count == 100
    assert report.features[0].provided_feature_name == "id"
    assert report.features[0].populated_count == 100


def test_round_trip_conversion():
    original_report = DataSubmissionReport(
        overview=DataSubmissionReportOverview(feature_count=100, features_flagged=5),
        features=[
            DataSubmissionReportFeature(
                provided_feature_name="id",
                nad_feature_name="id",
                populated_count=100,
                null_count=0,
            )
        ],
    )

    report_dict = report_to_dict(original_report)
    converted_report = report_from_dict(report_dict)

    assert (
        converted_report.overview.feature_count
        == original_report.overview.feature_count
    )
    assert (
        converted_report.features[0].provided_feature_name
        == original_report.features[0].provided_feature_name
    )
