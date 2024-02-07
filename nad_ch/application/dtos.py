from dataclasses import dataclass, asdict, field
from typing import List


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
        return {
            "overview": asdict(self.overview),
            "features": [asdict(feature) for feature in self.features],
        }
