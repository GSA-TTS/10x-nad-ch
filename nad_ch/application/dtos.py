from dataclasses import dataclass, asdict, field, is_dataclass
from typing import List
import numpy as np


@dataclass
class DownloadResult:
    temp_dir: str
    extracted_dir: str


@dataclass
class DataSubmissionReportOverview:
    feature_count: int = 0
    features_flagged: int = 0
    etl_update_required: bool = False
    data_update_required: bool = False


@dataclass
class DataSubmissionReportFeature:
    provided_feature_name: str
    nad_feature_name: str
    populated_count: int
    null_count: int


@dataclass
class DataSubmissionReport:
    overview: DataSubmissionReportOverview
    features: List[DataSubmissionReportFeature] = field(default_factory=list)

    def to_dict(self):
        # We need to make sure that every value in the DTO is JSON-serializable, so we
        # check each item recursively to convert any non "int" numbers to int
        def convert(item):
            if isinstance(item, dict):
                return {k: convert(v) for k, v in item.items()}
            elif isinstance(item, list):
                return [convert(i) for i in item]
            elif isinstance(item, (np.int64, np.int32, np.float64, np.float32)):
                return (
                    int(item)
                    if item.dtype == np.int64 or item.dtype == np.int32
                    else float(item)
                )
            elif is_dataclass(item):
                return convert(asdict(item))
            else:
                return item

        return convert(asdict(self))

    @classmethod
    def from_dict(cls, data: dict):
        overview_data = data.get("overview", {})
        features_data = data.get("features", [])

        overview = DataSubmissionReportOverview(**overview_data)

        features = [
            DataSubmissionReportFeature(**feature_data)
            for feature_data in features_data
        ]

        return cls(overview=overview, features=features)
